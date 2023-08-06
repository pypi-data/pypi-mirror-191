from ast import List, Tuple
from functools import wraps
from typing import Any, Callable, TypeVar
import pydantic
import requests
from urllib.parse import urljoin, urlencode

class GlooBaseClient:
    def __init__(
        self, origin: str, app_secret: str
    ) -> None:
        self.origin = origin.rstrip('/')
        self.app_secret = app_secret
        self.headers = {
            "Content-Type": "application/json",
            "X-Gloo-Auth-Key": app_secret,
        }

    def _post(self, path: str, *, data: pydantic.BaseModel | None):
        url = urljoin(self.origin, path) if path else self.origin
        response = requests.post(
            url=url,
            headers=self.headers,
            data=data.json(by_alias=True) if data else None,
        )
        if response.status_code >= 200 and response.status_code < 300:
            return response
        else:
            raise Exception(f"Received status code {response.status_code}")

    def _get(self, path: str, **kwargs):
        url = urljoin(self.origin, path) if path else self.origin
        params = urlencode(kwargs)
        if params:
            url += f"?{params}"
        response = requests.get(url=url, headers=self.headers)
        if response.status_code >= 200 and response.status_code < 300:
            return response
        else:
            raise Exception(f"Received status code {response.status_code}")
