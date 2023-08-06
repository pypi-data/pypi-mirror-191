import logging
import os

from numerous.image_tools.app import run_job
from numerous.image_tools.job import NumerousReportJob


class TestReport(NumerousReportJob):
    def __init__(self):
        super(TestReport, self).__init__()

    def add_report_content(self):
        prefix = "test report"
        self.report.add_info(
            title=f"{self.app.appname}",
            filename=" ".join([prefix, self.app.appname]),
            type_title=prefix,
            sub_title="Test",
            sub_sub_title="This is subtitle",
        )
        section = self.report.section(
            "Project",
            title=self.report.add_text(
                "project_sec_title", english=f"Project: {self.app.appname}"
            ),
        )

        div1 = self.report.div(classes="frame")

        figure1 = self.report.figure({"x": [0, 1, 2], "y": [2, 3, 9]})

        section.add_content({"subsection1": div1})

        div1.add_content({"figure": figure1})


def run_example():
    run_job(numerous_job=TestReport(), appname="test-report-example", model_folder=None)


if __name__ == "__main__":
    os.environ["LOG_LEVEL"] = "DEBUG"
    logging.basicConfig(level=logging.DEBUG)
    run_example()
