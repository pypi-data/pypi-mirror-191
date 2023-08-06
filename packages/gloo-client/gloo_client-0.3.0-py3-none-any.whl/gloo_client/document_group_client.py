from urllib.parse import urljoin
import requests
from gloo_client.model import (
    DocumentGroupResponse,
    DocumentGroupUpdateStatusRequest,
    DocumentGroupUpdateRequest,
    DocumentGroupCreateRequest,
)
from gloo_client.base_client import GlooBaseClient
from gloo_client.base_client import internal_only_api


class DocumentGroupClient(GlooBaseClient):
    def __init__(self, *, base: GlooBaseClient):
        super().__init__(
            origin=urljoin(base.origin, "/document_group"),
            api_key=base.api_key,
            internal_api_key=base.internal_api_key,
        )

    # Internal only API
    @internal_only_api
    def update_status(
        self, *, document_group_id: str, request: DocumentGroupUpdateStatusRequest
    ) -> DocumentGroupResponse:
        return DocumentGroupResponse.parse_raw(
            self._post(f"/{document_group_id}/status", data=request).text
        )

    def update(
        self, *, document_group_id: str, request: DocumentGroupUpdateRequest
    ) -> DocumentGroupResponse:
        return DocumentGroupResponse.parse_raw(
            self._post(f"/{document_group_id}", data=request).text
        )

    def create(self, *, request: DocumentGroupCreateRequest) -> DocumentGroupResponse:
        return DocumentGroupResponse.parse_raw(self._post(data=request).text)
