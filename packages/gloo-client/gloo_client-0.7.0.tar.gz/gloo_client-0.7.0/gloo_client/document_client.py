from urllib.parse import urljoin
import requests
from gloo_client.model import (
    DocumentResponse,
    DocumentUpdateMetadataRequest,
    DocumentUpdateRequest,
    DocumentCreateRequest,
)
from gloo_client.base_client import GlooBaseClient


class DocumentClient(GlooBaseClient):
    def __init__(self, *, base: GlooBaseClient, document_id: str):
        super().__init__(
            origin=urljoin(base.origin, f"/document/{document_id}"),
            app_secret=base.app_secret,
        )

    def update_metadata(
        self, *, request: DocumentUpdateMetadataRequest
    ) -> DocumentResponse:
        return DocumentResponse.parse_raw(
            self._post("/metadata", data=request).text
        )

    def update(
        self, *, request: DocumentUpdateRequest
    ) -> DocumentResponse:
        return DocumentResponse.parse_raw(
            self._post("/", data=request).text
        )

    def get(self) -> DocumentResponse:
        return DocumentResponse.parse_raw(self._get("/").text)
