import typing
from urllib.parse import urljoin
import requests
from gloo_client.model import (
    DocumentGroupResponse,
    DocumentGroupUpdateRequest,
    DocumentResponse,
    DocumentCreateRequest,
    Content,
    EmbeddingType
)
from gloo_client.base_client import GlooBaseClient


class DocumentGroupClient(GlooBaseClient):
    def __init__(self, *, base: GlooBaseClient, document_group_id: str):
        super().__init__(
            origin=urljoin(base.origin, f"document_group/{document_group_id}"),
            app_secret=base.app_secret
        )

    def get(self) -> DocumentGroupResponse:
        return DocumentGroupResponse.parse_raw(
            self._get(f"/").text
        )

    def update(
        self, *, name: str
    ) -> DocumentGroupResponse:
        return DocumentGroupResponse.parse_raw(
            self._post(f"/", data=DocumentGroupUpdateRequest(name=name)).text
        )

    def get_documents(self):
        return list(map(DocumentResponse.parse_obj, self._get(f"documents").json()))

    def create_document(self, *, source_url: str, name: str, content: typing.Union[str, typing.List[str]], tags: typing.List[str] = [], embedding_type: typing.Optional[EmbeddingType] = None):
        c = Content.factory.complete(content) if isinstance(content, str) else Content.factory.chunked(content)
        return DocumentResponse.parse_raw(self._post("create/document", data=DocumentCreateRequest(source_url=source_url, name=name, tags=tags, content=c, embedding_type=embedding_type)).text)
