from urllib.parse import urljoin
import requests
from gloo_client.model import (
    DocumentGroupResponse,
    DocumentGroupUpdateStatusRequest,
    DocumentGroupUpdateRequest,
    DocumentGroupCreateRequest,
    DocumentResponse,
    DocumentCreateRequest
)
from gloo_client.base_client import GlooBaseClient


class DocumentGroupClient(GlooBaseClient):
    def __init__(self, *, base: GlooBaseClient, document_group_id: str):
        super().__init__(
            origin=urljoin(base.origin, f"/document_group/{document_group_id}"),
            app_secret=base.app_secret
        )

    def get(
        self, *, request: DocumentGroupUpdateRequest
    ) -> DocumentGroupResponse:
        return DocumentGroupResponse.parse_raw(
            self._get(f"/", data=request).text
        )

    def update(
        self, *, request: DocumentGroupUpdateRequest
    ) -> DocumentGroupResponse:
        return DocumentGroupResponse.parse_raw(
            self._post(f"/", data=request).text
        )

    def get_documents(self):
        return list(map(DocumentResponse.parse_obj, self._get(f"/documents").json()))

    def create_document(self, *, request: DocumentCreateRequest):
        return DocumentResponse.parse_raw(self._post("/create/document", data=request).text)
