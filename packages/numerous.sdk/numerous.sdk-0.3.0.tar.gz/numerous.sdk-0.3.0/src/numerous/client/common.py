import logging
import threading
from collections import deque
from enum import Enum
from time import time
from typing import Callable, Iterator, Optional
from urllib.parse import urlparse

import grpc
from numerous.client_common.validation_interceptor import ValidationInterceptor

from . import config
from .config import GRPC_MAX_MESSAGE_SIZE

log = logging.getLogger("numerous.client")


class Interp(Enum):
    zero = 0
    linear = 1
    quadratic = 2


class JobStatus(Enum):
    ready = 0
    running = 1
    finished = 2
    request_termination = 3
    terminated = 4
    failed = 5
    requested = 6
    initializing = 7


class RepeatedFunction:
    def __init__(self, interval, function, run_initially=False, *args, **kwargs):
        self._timer: Optional[threading.Timer] = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time()

        if run_initially:
            self.function(*self.args, **self.kwargs)

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.next_call += self.interval
            self._timer = threading.Timer(self.next_call - time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        if self._timer is not None:
            self._timer.cancel()
        self.is_running = False


class RestorableIterator(Iterator):
    """
    Returns items not handled items again after restore.
    >>> restorable_iterator = RestorableIterator(iter(range(4)))
    >>> assert list(restorable_iterator) == [0, 1, 2, 3]
    >>> restorable_iterator.restore()
    >>> assert list(restorable_iterator) == [0, 1, 2, 3]
    >>> restorable_iterator.restore()
    >>> assert list(next(restorable_iterator) for i in range(3)) == [0, 1, 2]
    >>> restorable_iterator.item_handled()
    >>> restorable_iterator.item_handled()
    >>> restorable_iterator.restore()
    >>> assert list(restorable_iterator) == [2, 3]
    >>> restorable_iterator.item_handled()
    >>> restorable_iterator.restore()
    >>> assert list(restorable_iterator) == [3]
    >>> assert list(restorable_iterator) == []
    """

    def __init__(self, data: Iterator):
        self._not_handled: deque = deque()
        self._restored_data: deque = deque()
        self._data = data
        self._lock = threading.Lock()

    def __iter__(self):
        return self

    def __next__(self):
        with self._lock:
            next_item = (
                self._restored_data.popleft()
                if self._restored_data
                else next(self._data)
            )
            self._not_handled.append(next_item)
            return next_item

    def item_handled(self):
        with self._lock:
            self._not_handled.popleft()

    def restore(self):
        with self._lock:
            self._restored_data = self._not_handled + self._restored_data
            self._not_handled = deque()


def initialize_grpc_channel(
    refresh_token: str,
    token_callback: Callable[[], str],
    server: Optional[str] = None,
    port: Optional[int] = None,
    secure: Optional[bool] = None,
    instance_id: Optional[str] = None,
):
    secure_channel = secure if secure is not None else not config.FORCE_INSECURE
    if secure_channel is None:
        raise RuntimeError("Secure channel must be specified")
    server = server or config.NUMEROUS_API_SERVER
    if server is None:
        raise RuntimeError("Server must be specified")
    port = port or config.NUMEROUS_API_PORT
    if port is None:
        raise RuntimeError("Port must be specified")

    log.debug("Initializing gRPC channel %s:%s", server, port)

    options = [
        ("grpc.max_message_length", GRPC_MAX_MESSAGE_SIZE),
        ("grpc.max_send_message_length", GRPC_MAX_MESSAGE_SIZE),
        ("grpc.max_receive_message_length", GRPC_MAX_MESSAGE_SIZE),
    ]

    if secure_channel:
        creds = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(f"{server}:{port}", creds, options)
    else:
        channel = grpc.insecure_channel(f"{server}:{port}", options)

    vi = ValidationInterceptor(
        token=refresh_token, token_callback=token_callback, instance=instance_id
    )
    channel = grpc.intercept_channel(channel, vi)
    return channel, vi.instance


def parse_api_url(url: str):
    parsed_url = urlparse(url)
    server = parsed_url.hostname
    port = parsed_url.port or (443 if parsed_url.scheme == "https" else 80)
    secure = parsed_url.scheme == "https"
    return server, port, secure
