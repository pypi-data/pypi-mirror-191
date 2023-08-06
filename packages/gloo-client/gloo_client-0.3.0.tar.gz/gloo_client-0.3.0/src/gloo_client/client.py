import typing

import requests
from gloo_client.document_client import DocumentClient
from gloo_client.environment import GlooEnvironment
from gloo_client.model import SearchResultResponse, SearchRequest, PromptRequest
from gloo_client.document_group_client import DocumentGroupClient
from gloo_client.base_client import GlooBaseClient
from gloo_client.application_client import ApplicationClient


class GlooClient(GlooBaseClient):
    def __init__(
        self,
        environment: typing.Union[str, GlooEnvironment] = GlooEnvironment.Production,
        internal_api_key: str | None = None,
        *,
        api_key: str,
    ):
        if isinstance(environment, str):
            origin = environment
        else:
            origin = environment.value
        super().__init__(
            origin=origin, api_key=api_key, internal_api_key=internal_api_key
        )

        self.application = ApplicationClient(base=self)
        self.document_service = DocumentClient(base=self)
        self.document_group_service = DocumentGroupClient(base=self)

    def app(self) -> ApplicationClient:
        return self.application

    def document_group(self) -> DocumentGroupClient:
        return self.document_group_service

    def document(self) -> DocumentClient:
        return self.document_service

    def prompt(self, *, request: PromptRequest) -> typing.Any:
        return self._post("/prompt", data=request).json()

    def search(self, *, request: SearchRequest) -> SearchResultResponse:
        return SearchResultResponse(self._post("/search", data=request).text)
