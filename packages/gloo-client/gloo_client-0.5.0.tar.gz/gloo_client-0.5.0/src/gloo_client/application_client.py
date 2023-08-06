from urllib.parse import urljoin
from gloo_client.model import CreateApplicationResponse
from gloo_client.base_client import GlooBaseClient
from gloo_client.base_client import internal_only_api


class ApplicationClient(GlooBaseClient):
    def __init__(self, *, base: GlooBaseClient):
        super().__init__(
            origin=urljoin(base.origin, "/application"),
            api_key=base.api_key,
            internal_api_key=base.internal_api_key,
        )

    def get(self) -> None:
        return self._get("/")

    @internal_only_api
    def create(self) -> CreateApplicationResponse:
        return CreateApplicationResponse.parse_raw(self._post(f"/", data=None).text)
