import time
from collections.abc import Awaitable, Callable
from typing import Literal, Optional

import structlog
from django import http

GetResponse = Callable[
    [http.HttpRequest],
    http.response.HttpResponseBase | Awaitable[http.response.HttpResponseBase],
]


logger = structlog.get_logger(__name__)

START_TIME_ATTRIBUTE = "start_time"


def get_start_time(request: http.HttpRequest, /) -> Optional[float]:
    return getattr(request, START_TIME_ATTRIBUTE, None)


def set_start_time(request: http.HttpRequest, /) -> None:
    setattr(request, START_TIME_ATTRIBUTE, time.time())


def calculate_request_duration(start_time: float, /) -> tuple[int, Literal["ms"]]:
    # Convert to milliseconds and an integer.
    duration = int((time.time() - start_time) * 1000)
    return duration, "ms"


class StartTimer:
    def __init__(
        self,
        get_response: GetResponse,
    ) -> None:
        self.get_response = get_response

    def __call__(self, request: http.HttpRequest) -> http.response.HttpResponseBase:
        set_start_time(request)
        return self.get_response(request)


class StopTimer:
    def __init__(
        self,
        get_response: GetResponse,
    ) -> None:
        self.get_response = get_response

    def __call__(self, request: http.HttpRequest) -> http.response.HttpResponseBase:
        response = self.get_response(request)
        duration = self.get_duration_milliseconds(request)
        if duration is not None:
            structlog.contextvars.bind_contextvars(request_duration=duration)
        return response

    def get_duration_milliseconds(self, request: http.HttpRequest, /) -> Optional[str]:
        start_time = get_start_time(request)
        if start_time is not None:
            duration, unit = calculate_request_duration(start_time)
            return f"{duration}{unit}"
        return None
