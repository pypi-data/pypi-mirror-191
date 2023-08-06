import typing
from urllib.parse import urljoin
from gloo_client.model import CompletionRequest, CompletionResponse, SearchRequest, SearchResultResponse, DocumentGroupResponse, DocumentGroupCreateRequest
from gloo_client.base_client import GlooBaseClient
from gloo_client.model import DocumentGroupResponse
from gloo_client.document_client import DocumentClient
from gloo_client.document_group_client import DocumentGroupClient


class AppClient(GlooBaseClient):
    def __init__(self, *, base: GlooBaseClient, app_id: str):
        super().__init__(
            origin=urljoin(base.origin, f"/app/{app_id}"),
            app_secret=base.app_secret
        )

    def document_group(self, *, document_group_id: str):
        return DocumentGroupClient(base=self, document_group_id=document_group_id)

    def document(self, *, document_id: str):
        return DocumentClient(base=self, document_id=document_id)

    def get(self) -> None:
        self._get("/")

    def completion(self, *, data: CompletionRequest):
        return CompletionResponse.parse_raw(self._post(f"/completion", data=data).text)

    def search(self, *, data: SearchRequest):
        return SearchResultResponse.parse_raw(self._post(f"/search", data=data).text)

    def document_groups(self):
        return list(map(DocumentGroupResponse.parse_obj, self._get(f"/document_groups").json()))

    def create_document_group(self, *, data: DocumentGroupCreateRequest):
        return DocumentGroupResponse.parse_raw(self._get(f"/document_groups").text)
