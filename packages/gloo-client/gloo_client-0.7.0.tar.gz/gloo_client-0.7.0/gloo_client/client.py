import typing

import requests
from gloo_client.document_client import DocumentClient
from gloo_client.environment import GlooEnvironment
from gloo_client.model import CreateApplicationRequest, CreateApplicationResponse
from gloo_client.document_group_client import DocumentGroupClient
from gloo_client.base_client import GlooBaseClient
from gloo_client.app_client import AppClient


class GlooClient(GlooBaseClient):
    def __init__(
        self,
        environment: typing.Union[str, GlooEnvironment] = GlooEnvironment.Production,
        *,
        app_secret: str,
    ):
        if isinstance(environment, str):
            origin = environment
        else:
            origin = environment.value
        super().__init__(
            origin=origin, app_secret=app_secret
        )

    def app(self,*, app_id: str):
        return AppClient(base=self, app_id=app_id)

    def create_app(self, *, data: CreateApplicationRequest):
        return CreateApplicationResponse.parse_raw(self._post('/create/app', data=data).text)
        