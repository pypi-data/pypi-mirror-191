import json
from pathlib import Path
from typing import List, Optional, Union

from datagen.api.assets import Background, Camera, DataRequest, Glasses, Human, HumanDatapoint, Light, Mask

# from datagen.api.client.impl import DataGenerationClient
# from datagen.api.client.schemas import DataResponse, DataResponseStatus
from datagen.api.requests.datapoint.builder import HumanDatapointBuilder
from datagen.api.requests.director import DataRequestDirector
from datagen.dev.logging import get_logger

logger = get_logger(__name__)

DEFAULT_DATAPOINT_REQUESTS_JSON_NAME = "datagen_data_request.json"


class DatagenAPI:
    def __init__(
        self,
        # client: DataGenerationClient,
    ):
        self._request_director = DataRequestDirector()
        # self._client = client

    def create_datapoint(
        self,
        human: Human,
        camera: Camera,
        glasses: Optional[Glasses] = None,
        mask: Optional[Mask] = None,
        background: Optional[Background] = None,
        lights: Optional[List[Light]] = None,
    ) -> HumanDatapoint:
        self._request_director.builder = HumanDatapointBuilder(human, camera, glasses, mask, background, lights)
        return self._request_director.build_datapoint()

    # def generate(self, request: DataRequest) -> DataResponse:
    #     return self._client.generate(request)
    #
    # def stop(self, generation_id: str) -> None:
    #     return self._client.stop(generation_id=generation_id)
    #
    # def get_status(self, generation_id: str) -> DataResponseStatus:
    #     return self._client.get_status(generation_id=generation_id)
    #
    # def get_download_urls(self, generation_id: str) -> List[str]:
    #     return self._client.get_download_urls(generation_id=generation_id)
    #
    # def download(self, urls: List[str], dest: str) -> None:
    #     self._client.download(urls=urls, dest=Path(dest))

    def load(self, path: Union[Path, str]) -> DataRequest:
        if not isinstance(path, Path):
            path = self._get_request_json_path(path)
        path = self._get_request_json_path(path)
        return DataRequest.parse_file(path)

    def dump(self, request: DataRequest, path: Union[Path, str] = None) -> None:
        if not isinstance(path, Path):
            path = self._get_request_json_path(path)
        path.write_text(json.dumps(request.dict(), indent=3, sort_keys=True))
        logger.info(
            "Request was successfully dumped to path '{path}' ({num} datapoints total).",
            path=path_.absolute(),
            num=len(request),
        )

    def _get_request_json_path(self, path: Optional[str]) -> Path:
        path_ = Path(path) if path else Path.cwd().joinpath(DEFAULT_DATAPOINT_REQUESTS_JSON_NAME)
        if not path_.parent.exists():
            raise FileNotFoundError(f"{path_.parent} folder does not exist, cannot dump requests")
        return path_
