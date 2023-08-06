import datetime

import ipywidgets as widgets
import plotly.graph_objects as go
from jinja2 import Template
from plotly.graph_objs import FigureWidget

caption_numbers = {"Figure": [0, {}], "Table": [0, {}]}


def num_caption(id_, captions, caption_type="Figure"):
    specific_caption_numbers = caption_numbers[caption_type]

    if id_ not in specific_caption_numbers[1]:
        specific_caption_numbers[0] += 1
        specific_caption_numbers[1][id_] = specific_caption_numbers[0]

    this_number = specific_caption_numbers[0]

    caption = (
        '<div id="caption_"'
        + str(id_)
        + ' class="caption">'
        + caption_type
        + " "
        + str(this_number)
        + ": "
    )

    caption = caption + captions[0] + "</div>"

    if len(captions) > 1 and captions[1]:
        caption = (
            caption
            + '<div id="note_"'
            + str(id_)
            + ' class="note"><i>Note: '
            + captions[1]
            + "</i></div>"
        )

    return '<div class="caption-section">' + caption + "</div>"


language = "english"

text: dict[str, dict[str, str]] = {}


def get_text(key, language=language):
    return text[key][language]


def gs(state, key, default=0):
    return state[key] if (state and key in state) else default


# Style to add to widgets to make description text show by resizing value area
style = {"description_width": "initial"}


class Report:
    def __init__(
        self, uploader, upload_on_set_content=True, debounce_upload=10, template=None
    ):
        self.upload_on_set_content = upload_on_set_content

        self.debound_upload = debounce_upload
        self.last_upload_time = datetime.datetime(2000, 1, 1)

        self.contents = {}
        self.template = template

        self.uploader = uploader
        self.children = {}

    def add_info(self, title, sub_title, sub_sub_title, filename, type_title):
        # self.author = author
        # self.author_email = author_email
        self.title = title
        self.filename = filename
        self.report_data = dict(
            report_type_title=type_title,
            report_title=title,
            report_sub_title=sub_title,
            report_sub_sub_title=sub_sub_title,
            # report_author = f'<a href="mailto:{author_email}">{author}</a>',
            report_date="{: %d-%m-%Y}".format(datetime.datetime.now()),
            report_header=type_title,
        )

    def section(self, id_, title, content=None, mute=False, display_level=10):
        sec = Section(
            state={"title": title},
            children=content,
            mute=mute,
            display_level=display_level,
        )
        self.children[id_] = sec
        if content:
            self.upload()
        return sec

    def upload(
        self, force=False, display_level=10, hide={}, filename=None, file_id="default"
    ):
        if filename is None:
            filename = self.filename

        if (
            self.upload_on_set_content
            and datetime.datetime.now()
            > self.last_upload_time + datetime.timedelta(seconds=self.debound_upload)
        ) or force:
            self.save(display_level=display_level, hide=hide, filename=filename)

            self.last_upload_time = datetime.datetime.now()

            self.uploader(filename + ".html", file_id)

    def render(self):
        if self.state:
            self.apply_state(self.state)

        for c in self.children.values():
            c.render()

        children_widgets = []
        for c in self.children.values():
            if not c.mute:
                children_widgets.append(c.widget)

        super().__init__([], children_widgets, editor_below=False)

    def get_state(self):
        # return state
        return {"children": {c.id_: c.get_state() for c in self.children}}

    def apply_state(self, state):
        children_state = gs(state, "children", {})

        for c_id_, c in self.children.items():
            if c_id_ in children_state:
                c.apply_state(children_state[c_id_])

    def as_html(self, display_level=0, hide={}):
        if len(list(self.children.values())) > 0:
            html = "".join(
                [
                    c.as_html(display_level=display_level, hide=hide)
                    for id_, c in self.children.items()
                    if id_ not in hide
                ]
            )

            with open(self.template, "r") as tf:
                template_str = tf.read()

            t = Template(template_str)

            rendered = t.render(report_content=html, **self.report_data)
            return rendered
        else:
            return ""

    def save(self, display_level=0, hide={}, filename=None):
        if filename is None:
            filename = self.filename
        f_ = open(filename + ".html", "w")

        f_.write(self.as_html(display_level=display_level, hide=hide))
        f_.close()

    def finalize(self, display_level=0, hide={}, filename=None, file_id="default"):
        self.upload(
            force=True,
            display_level=display_level,
            hide=hide,
            filename=filename,
            file_id=file_id,
        )

    def add_text(self, key=None, **kwargs):
        if key:
            text[key] = kwargs
            if language in kwargs:
                return text[key][language]
            else:
                return list(text[key].values())[0]
        else:
            if language in kwargs:
                return kwargs[language]
            else:
                return list(kwargs.values())[0]

    def figure(
        self,
        figure_data={},
        state={"caption": "", "notes": ""},
        mute=False,
        post_script=None,
        display_level=10,
    ):
        return Figure(
            figure_data=figure_data,
            state=state,
            mute=mute,
            post_script=post_script,
            display_level=display_level,
        )

    def div(self, mute=False, state={}, display_level=10, classes=None):
        return Div(mute=mute, state=state, display_level=display_level, classes=classes)

    def table(
        self,
        table_df,
        state={"caption": "", "notes": ""},
        mute=False,
        display_level=10,
        classes=None,
        caption=True,
        index=True,
    ):
        return Table(
            table_df,
            state=state,
            mute=mute,
            display_level=display_level,
            classes=classes,
            caption=caption,
            index=index,
        )

    def tabs(self, state={"title": ""}, children=None, mute=False, display_level=10):
        return Tabs(
            state=state, children=children, mute=mute, display_level=display_level
        )


class Block:
    def __init__(
        self,
        editor_widgets,
        view_widgets,
        editor_below=False,
        name="unnamed",
        edit_list_class=None,  # noqa: F841
        wrap_class=None,
        display_level=10,
    ):
        # name used to identify the block - non-unique
        self.name = name
        self.display_level = display_level
        self.classes = None
        # list of editor widhgets to go in accordion (fold/unfold widget)
        self.editor_widgets = editor_widgets

        # the editor itself - selected index is not so it is closed by starting point
        self.editor = widgets.Accordion(
            (widgets.VBox(editor_widgets),), selected_index=None
        )

        # the view part - containing widgets always to be visible
        self.view = [widgets.VBox(view_widgets)]

        # Only add editor if it has widgets
        if len(editor_widgets) > 0:
            # check if editor should be above or below view
            if editor_below:
                widgets_list = self.view + [self.editor]

            else:
                widgets_list = [self.editor] + self.view

        else:
            # only adding view widgets
            widgets_list = self.view

        # Check if this widget should be wrapped with another widget class like accordion or so
        if wrap_class:
            # wrap class makes it simple to enclose ie a list of blocks in individual accordions
            # this way you can keep multiple items in list open at same time.
            self.widget = wrap_class((widgets.VBox(widgets_list),))
        else:
            self.widget = widgets.VBox(widgets_list)

    # default method called to show the block widget - do not overwrite unless calling super().show() end the end
    def show(self):
        # TODO: figure out what this function should do
        # display(self.widget)
        pass

    def render(self):
        pass

    # String rep of this class is just its name
    def __str__(self):
        return self.name


def wrap_div(html, class_=None):
    if class_:
        return f"<div class='{class_}'>\n{html}\n</div>\n"
    else:
        return f"<div>\n{html}\n</div>\n"


class Section(Block):
    def __init__(
        self, state={"title": ""}, children=None, mute=False, display_level=10
    ):
        self.mute = mute
        self.display_level = display_level
        self.state = state
        self.children = {}
        if children:
            self.set_content(children)

    def set_content(self, content):
        self.children = content

        for c_id_, c in self.children.items():
            c.set_id(c_id_)

    def add_content(self, content: dict):
        self.children.update(content)

        for c_id_, c in self.children.items():
            c.set_id(c_id_)

    def set_id(self, id_):
        self.id_ = id_

    def render(self):
        if not self.mute:
            # Widgets - initiate
            self.Title_widget = widgets.Textarea("", description="Title:", style=style)
            self.html_widget = widgets.HTML("")

            def update_html(e):
                self.html_widget.value = self.title_as_html()
                self.state["title"] = self.Title_widget.value

            self.Title_widget.observe(update_html)

            # Assign all widgets to view section of block

            if self.state:
                self.apply_state(self.state)

            for c in self.children.values():
                c.render()

            children_widgets = []
            for c in self.children.values():
                if not c.mute:
                    children_widgets.append(c.widget)

            super().__init__(
                [self.Title_widget],
                [widgets.VBox([self.html_widget] + children_widgets)],
                editor_below=False,
            )

    def get_state(self):
        # return state

        self.state.update(
            {"children": {c.id_: c.get_state() for c in self.children.values()}}
        )
        return self.state

    def apply_state(self, state):
        self.Title_widget.value = gs(state, "title", "My Report Title")
        children_state = gs(state, "children", {})

        for c_id_, c in self.children.items():
            if c_id_ in children_state:
                c.apply_state(children_state[c_id_])

    def title_as_html(self):
        return (
            "<h1 id='sec_title_"
            + gs(self.state, "title", "")
            + "' class='section_title'>"
            + gs(self.state, "title", "")
            + "</h1>"
        )

    def as_html(self, display_level=0, hide={}):
        show_ = (
            not self.mute
            and self.display_level >= display_level
            and len(list(self.children.values())) > 0
        )
        if show_:
            html = wrap_div(
                wrap_div(self.title_as_html())
                + "".join(
                    [c.as_html() for id_, c in self.children.items() if id_ not in hide]
                ),
                class_="section"
                + ", "
                + gs(self.state, "title", "").replace(" ", "_").lower(),
            )
            return html
        else:
            return ""


class Tabs(Block):
    def __init__(
        self, state={"title": ""}, children=None, mute=False, display_level=10
    ):
        self.display_level = display_level
        self.mute = mute

        self.state = state
        self.children = {}
        if children:
            self.set_content(children)

    def add_tab(self, content):
        self.children.update(content)
        for c_id_, c in self.children.items():
            c.set_id(c_id_)

    def set_id(self, id_):
        self.id_ = id_

    def render(self):
        if not self.mute:
            # Widgets - initiate
            self.Title_widget = widgets.Textarea("", description="Title:", style=style)
            self.html_widget = widgets.HTML("")

            def update_html(e):
                self.html_widget.value = self.title_as_html()
                self.state["title"] = self.Title_widget.value

            self.Title_widget.observe(update_html)

            # Assign all widgets to view section of block

            if self.state:
                self.apply_state(self.state)

            for c in self.children.values():
                c.render()

            children_widgets = []
            for c in self.children.values():
                if not c.mute:
                    children_widgets.append(c.widget)

            super().__init__(
                [self.Title_widget],
                [widgets.VBox([self.html_widget] + children_widgets)],
                editor_below=False,
            )

    def get_state(self):
        # return state

        self.state.update(
            {"children": {c.id_: c.get_state() for c in self.children.values()}}
        )
        return self.state

    def apply_state(self, state):
        self.Title_widget.value = gs(state, "title", "My Report Title")
        children_state = gs(state, "children", {})

        for c_id_, c in self.children.items():
            if c_id_ in children_state:
                c.apply_state(children_state[c_id_])

    def as_html(self, display_level=0, hide={}):
        tablist = list(self.children.keys())
        show_ = (
            not self.mute and self.display_level >= display_level and len(tablist) > 0
        )
        if show_:
            tab_script = (
                """<script>
                    function openTab_"""
                + self.id_
                + """(evt, tabname) {
                      var i, tabcontent, tablinks;
                      tabcontent = document.getElementById('"""
                + self.id_
                + """').getElementsByClassName("tabcontent");

                      for (i = 0; i < tabcontent.length; i++) {

                        tabcontent[i].style.display = "none";
                      }

                      tablinks = document.getElementById('"""
                + self.id_
                + """').getElementsByClassName("tablinks");
                      for (i = 0; i < tablinks.length; i++) {
                        tablinks[i].className = tablinks[i].className.replace(" active", "");
                      }
                      thistab = document.getElementById(tabname);
                      //thistab.style.width= '100%';
                      thistab.style.display = "block";
                      //window.dispatchEvent(new Event('resize'));
                      evt.currentTarget.className += " active";
                    }
                    var evt = document.createEvent("MouseEvents");
                    evt.initMouseEvent("click", true, true, window, 1, 0, 0, 0, 0,
                        false, false, false, false, 0, null);

                    document.getElementById('default_tab_"""
                + self.id_
                + """').dispatchEvent(evt);
                    </script>"""
            )
            tab_divs = []
            tab_buttons = []
            i = 0
            for t, c in self.children.items():
                if t not in hide:
                    label = c.get_state()["label"]
                    tab_label = (
                        f"""<button id=default_tab_{self.id_} class="tablinks" """
                        f"""onclick="openTab_{self.id_}(event, 'tab_{t}')">{label}</button>"""
                    )
                    if i > 0:
                        tab_div = f"""
                        <div id="tab_{t}" class="tabcontent" style="display: block;" width="100%">
                              {c.as_html()}
                        </div>"""
                    else:
                        tab_div = f"""
                        <div id="tab_{t}" class="tabcontent" style="display: block;" width="100%">
                              {c.as_html()}
                        </div>"""
                        i += 1
                    tab_divs.append(tab_div)
                    tab_buttons.append(tab_label)

            buttons = "".join(tab_buttons)
            tabs = "".join(tab_divs)
            html = f'<div id="{self.id_}"><div class="tab">{buttons}</div>{tabs}</div>{tab_script}'

            return html
        else:
            return ""


class Div(Block):
    def __init__(
        self, mute=False, state={}, display_level=10, children=None, classes=None
    ):
        self.mute = mute
        self.display_level = display_level
        # Widgets - initiate
        self.state = state
        self.html = ""
        self.classes = classes
        self.children = {}
        if children:
            self.set_content(children)

    def set_id(self, id_):
        self.id_ = id_

    def set_content(self, content):
        self.children = content

        for c_id_, c in self.children.items():
            c.set_id(c_id_)

    def add_content(self, content: dict):
        self.children.update(content)

        for c_id_, c in self.children.items():
            c.set_id(c_id_)

    def render(self):
        if not self.mute:
            self.html_widget = widgets.HTML(self.html)

            # Assign all widgets to view section of block
            super().__init__([], [self.html_widget])

    def get_state(self):
        # return state
        return self.state

    def apply_state(self, state):
        pass

    def as_html(self, display_level=0, hide={}):
        show_ = not self.mute and self.display_level >= display_level
        for id_, c in self.children.items():
            self.html += c.as_html() + "\n"
        return wrap_div(self.html, self.classes) if show_ else ""


class Figure(Block):
    def __init__(
        self,
        figure_data={},
        state={"caption": "", "notes": ""},
        mute=False,
        post_script=None,
        display_level=10,
    ):
        self.display_level = display_level
        self.mute = mute
        self.post_script = post_script
        # Widgets - initiate
        self.state = state
        self.figure_data = figure_data

    def set_id(self, id_):
        self.id_ = id_

    def render(self):
        if not self.mute:
            self.html_widget = widgets.HTML()

            self.graph_widget = FigureWidget(self.figure_data)

            self.caption_widget = widgets.Text(
                gs(self.state, "caption", ""), description="Caption:", style=style
            )
            self.notes_widget = widgets.Textarea(
                gs(self.state, "notes", ""), description="Notes:", style=style
            )

            def update_html(e):
                self.state = {
                    "caption": self.caption_widget.value,
                    "notes": self.notes_widget.value,
                }

                self.html_widget.value = self.caption_notes_html()

            # print(self.html_widget.value )

            self.caption_widget.observe(update_html)
            self.notes_widget.observe(update_html)

            update_html(None)

            # Assign all widgets to view section of block
            super().__init__(
                [self.caption_widget, self.notes_widget],
                [widgets.VBox([self.graph_widget, self.html_widget])],
                editor_below=True,
            )

            if self.state:
                self.apply_state(self.state)

    def get_state(self):
        # return state
        return self.state

    def apply_state(self, state):
        # self.html_widget.value = gs(state, 'figure_html', "")
        self.caption_widget.value = gs(state, "caption", "")
        self.notes_widget.value = gs(state, "notes", "")

    def caption_notes_html(self):
        return num_caption(
            self.id_,
            [gs(self.state, "caption", ""), gs(self.state, "notes", "")],
            caption_type="Figure",
        )

    def as_html(self, display_level=0, hide={}):
        show_ = not self.mute and self.display_level >= display_level
        if show_:
            html = (
                wrap_div(
                    go.Figure(self.figure_data).to_html(
                        config={"displayModeBar": True},
                        # show_link=False,
                        include_plotlyjs=False,
                        # output_type='div',
                        full_html=False,
                        post_script=self.post_script,
                    ),
                    class_="figure_div",
                )
                + self.caption_notes_html()
            )

            return html
        else:
            return ""


class Table(Block):
    def __init__(
        self,
        table_df,
        state={"caption": "", "notes": ""},
        mute=False,
        display_level=10,
        classes=None,
        caption=True,
        index=True,
    ):
        self.display_level = display_level
        self.mute = mute

        # Widgets - initiate
        self.state = state
        self.table_df = table_df
        self.classes = classes
        self.caption = caption
        self.index = index

    def set_id(self, id_):
        self.id_ = id_

    def render(self):
        if not self.mute:
            self.html_widget = widgets.HTML()

            self.caption_widget = widgets.Text(
                gs(self.state, "caption", ""), description="Caption:", style=style
            )
            self.notes_widget = widgets.Textarea(
                gs(self.state, "notes", ""), description="Notes:", style=style
            )

            def update_html(e):
                self.state = {
                    "caption": self.caption_widget.value,
                    "notes": self.notes_widget.value,
                }
                self.html_widget.value = self.caption_notes_html()

            # print(self.html_widget.value )

            self.caption_widget.observe(update_html)
            self.notes_widget.observe(update_html)

            update_html(None)

            # Assign all widgets to view section of block
            super().__init__(
                [self.caption_widget, self.notes_widget],
                [widgets.VBox([self.html_widget])],
                editor_below=True,
            )

            if self.state:
                self.apply_state(self.state)

    def get_state(self):
        # return state
        return self.state

    def apply_state(self, state):
        # self.html_widget.value = gs(state, 'figure_html', "")
        self.caption_widget.value = gs(state, "caption", "")
        self.notes_widget.value = gs(state, "notes", "")

    def caption_notes_html(self):
        if self.caption:
            return self.table_df.to_html(classes=self.classes) + num_caption(
                self.id_,
                [gs(self.state, "caption", ""), gs(self.state, "notes", "")],
                caption_type="Table",
            )
        else:
            return self.table_df.to_html(classes=self.classes, index=self.index)

    def as_html(self, display_level=0, hide={}):
        show_ = not self.mute and self.display_level >= display_level
        if show_:
            return self.caption_notes_html()
        else:
            return ""
