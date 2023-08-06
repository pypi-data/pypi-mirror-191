import typing
from urllib.parse import urljoin
from gloo_client.model import CompletionRequest, CompletionResponse, SearchRequest, SearchResultResponse, DocumentGroupResponse, DocumentGroupCreateRequest, EmbeddingType
from gloo_client.base_client import GlooBaseClient
from gloo_client.model import DocumentGroupResponse
from gloo_client.document_client import DocumentClient
from gloo_client.document_group_client import DocumentGroupClient


class AppClient(GlooBaseClient):
    def __init__(self, *, base: GlooBaseClient, app_id: str):
        super().__init__(
            origin=urljoin(base.origin, f"app/{app_id}"),
            app_secret=base.app_secret
        )

    def document_group(self, *, document_group_id: str):
        return DocumentGroupClient(base=self, document_group_id=document_group_id)

    def document(self, *, document_id: str):
        return DocumentClient(base=self, document_id=document_id)

    def get(self) -> None:
        self._get("")

    def completion(self, *, prompt: str):
        return CompletionResponse.parse_raw(self._post(f"completion", data=CompletionRequest(prompt=prompt)).text)

    def search(self, *, query: str, max_content_size: typing.Optional[int] = None, tags: typing.Optional[typing.List[str]] = None, embedding_type: typing.Optional[EmbeddingType] = None):
        return SearchResultResponse.parse_raw(self._post(f"search", data=SearchRequest(query=query, embedding_type=embedding_type, max_content_size=max_content_size, tags=tags)).text)

    def document_groups(self):
        return list(map(DocumentGroupResponse.parse_obj, self._get(f"document_groups").json()))

    def create_document_group(self, *, source_url: str, name: str):
        return DocumentGroupResponse.parse_raw(self._post(f"create/document_group", data=DocumentGroupCreateRequest(source_url=source_url, name=name)).text)
