import functools
from typing import Callable
import requests
from ..connection import prepare_request, send_request


def http_factory(fn):
    @functools.wraps(fn)
    def factory(add_token: Callable[[requests.models.Request], requests.models.Request]):
        def inner(*args, **kwargs):
            request = fn(*args, **kwargs)
            return send_request(
                add_token(prepare_request(request))
            )
        return inner
    return factory
