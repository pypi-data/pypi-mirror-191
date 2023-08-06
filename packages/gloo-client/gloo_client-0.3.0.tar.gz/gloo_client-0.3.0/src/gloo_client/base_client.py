from ast import Tuple
from functools import wraps
from typing import Any, TypeVar
import pydantic
import requests
from urllib.parse import urljoin, urlencode

T = TypeVar("T")


def internal_only_api(func: T) -> T:
    @wraps(func)
    def wrapper(self: "GlooBaseClient", *args: Tuple[Any, ...], **kwargs: Any):
        if self.internal_api_key is None:
            raise NotImplementedError("This is an internal only api")
        return func(self, *args, **kwargs)

    wrapper.__annotations__ = func.__annotations__
    wrapper.__doc__ = (
        "Internal use only. Clients should not depend on it in any way.\n\n"
        + func.__doc__
        if func.__doc__
        else "Internal use only. Clients should not depend on it in any way."
    )
    return wrapper


class GlooBaseClient:
    def __init__(
        self, origin: str, api_key: str, internal_api_key: str | None = None
    ) -> None:
        self.origin = origin if origin.endswith("/") else origin + "/"
        self.api_key = api_key
        self.internal_api_key = internal_api_key
        self.headers = {
            "Content-Type": "application/json",
            "X-Gloo-Api-Key": api_key,
        }
        if internal_api_key:
            self.headers.update({"X-Gloo-Internal-Key": internal_api_key})

    def _post(self, path: str, *, data: pydantic.BaseModel | None):
        response = requests.post(
            url=urljoin(self.origin, path),
            headers=self.headers,
            data=data.json(by_alias=True) if data else None,
        )
        if response.status_code >= 200 and response.status_code < 300:
            return response
        else:
            raise Exception(f"Received status code {response.status_code}")

    def _get(self, path: str, **kwargs):
        url = urljoin(self.origin, path)
        params = urlencode(kwargs)
        if params:
            url += f"?{params}"
        response = requests.get(url=url, headers=self.headers)
        if response.status_code >= 200 and response.status_code < 300:
            return response
        else:
            raise Exception(f"Received status code {response.status_code}")
