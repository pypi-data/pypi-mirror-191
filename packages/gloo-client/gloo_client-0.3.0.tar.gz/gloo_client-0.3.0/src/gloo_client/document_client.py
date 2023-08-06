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
    def __init__(self, *, base: GlooBaseClient):
        super().__init__(
            origin=urljoin(base.origin, "/document"),
            api_key=base.api_key,
            internal_api_key=base.internal_api_key,
        )

    def update_metadata(
        self, *, document_id: str, request: DocumentUpdateMetadataRequest
    ) -> DocumentResponse:
        return DocumentResponse.parse_raw(
            self._post(f"/{document_id}/metadata", data=request).text
        )

    def update(
        self, *, document_id: str, request: DocumentUpdateRequest
    ) -> DocumentResponse:
        return DocumentResponse.parse_raw(
            self._post(f"/{document_id}", data=request).text
        )

    def create(self, *, request: DocumentCreateRequest) -> DocumentResponse:
        return DocumentResponse.parse_raw(self._post(data=request).text)
