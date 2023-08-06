import typing
from urllib.parse import urljoin
import requests
from gloo_client.model import (
    DocumentResponse,
    DocumentUpdateMetadataRequest,
    DocumentUpdateRequest,
    EmbeddingType,
    Content
)
from gloo_client.base_client import GlooBaseClient


class DocumentClient(GlooBaseClient):
    def __init__(self, *, base: GlooBaseClient, document_id: str):
        super().__init__(
            origin=urljoin(base.origin, f"/document/{document_id}"),
            app_secret=base.app_secret,
        )

    def update_metadata(
        self, *, tags: typing.Optional[typing.List[str]] = None, name: typing.Optional[str]
    ) -> DocumentResponse:
        return DocumentResponse.parse_raw(
            self._post("/metadata", data=DocumentUpdateMetadataRequest(tags=tags, name=name)).text
        )

    def update(
        self, *, content: typing.Optional[typing.Union[str, typing.List[str]]] = None, embedding_type: typing.Optional[EmbeddingType] = None
    ) -> DocumentResponse:
        
        c = Content.factory.complete(content) if isinstance(content, str) else Content.factory.chunked(content) if isinstance(content, list) else None

        return DocumentResponse.parse_raw(
            self._post("/", data=DocumentUpdateRequest(embedding_type=embedding_type, content=c)).text
        )

    def get(self) -> DocumentResponse:
        return DocumentResponse.parse_raw(self._get("/").text)
