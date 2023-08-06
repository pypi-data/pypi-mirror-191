import threading
import traceback
from datetime import datetime
from queue import Queue
from time import time

from .common import log


class NumerousBufferedWriter:
    def __init__(
        self,
        write_method,
        writer_closed_method,
        scenario: str,
        buffer_size: int = 24 * 7,
    ):
        self.scenario = scenario
        self._tags = None
        self.ix = 0
        self._write_method = write_method
        self._writer_closed = writer_closed_method
        self._buffer = None
        self.buffer_size = buffer_size
        self.write_queue: Queue = Queue()
        self.closed = False

        self.last_flush = time()
        self.max_elapse_flush = 600
        self.min_elapse_flush = 1
        self.force_flush = False

        self.buffer_number_size = 1e6

        self.writer_thread = threading.Thread(target=self._writer_thread_func)
        self.writer_thread.start()

    def _write_generator(self):
        while True:
            row = self.write_queue.get()
            if row == "STOP":
                return
            yield row

    def _writer_thread_func(self):
        not_done = True
        while not_done:
            try:
                self._write_method(self._write_generator(), must_flush=self._must_flush)
                not_done = False
            except Exception:
                tb = traceback.format_exc()
                log.error(tb)
                raise KeyboardInterrupt("Writer failed")

    def _must_flush(self, n_rows, rows_size):
        tic = time()
        buffer_counter = rows_size * n_rows
        if self.force_flush:
            self.force_flush = False
            self.last_flush = tic
            return True
        elif (
            n_rows > self.buffer_size
            and tic > self.min_elapse_flush + self.last_flush
            or buffer_counter > self.buffer_number_size
        ):
            self.last_flush = tic
            return True
        elif tic > (self.last_flush + self.max_elapse_flush):
            self.last_flush = tic
            return True
        return False

    def _init_buffer(self):
        self._buffer_count = 0
        # self._buffer = {t: [] for t in self._tags}
        self._buffer_timestamp = []

    def write_row(self, data):
        if "_index" not in data:
            data["_index"] = self.ix
            self.ix += 1

        if isinstance(data["_index"], datetime):
            data["_index"] = data["_index"].timestamp()
        if self.closed:
            raise ValueError("Queue is closed!")
        self.write_queue.put(data)
        return data["_index"]

    def flush(self):
        self.force_flush = True
        # self._write_method(self._buffer, self.scenario)
        self._init_buffer()

    def close(self):
        if not self.closed:
            self.flush()

            self.write_queue.put("STOP")

            self.writer_thread.join()

            self._writer_closed(self.scenario)

        self.closed = True
