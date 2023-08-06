import concurrent.futures
import json
import urllib.parse
from dataclasses import dataclass
from http import HTTPStatus
from pathlib import Path
from typing import List

import requests

from datagen.api.assets import DataRequest, HumanDatapoint
from datagen.api.client.exceptions import HttpStatusHandler
from datagen.api.client.schemas import DataResponse, DataResponseStatus
from datagen.config import settings
from datagen.dev.logging import get_logger

logger = get_logger(__name__)


@dataclass
class AuthenticationConfig:
    token: str
    user_id: str
    org_id: str


class DataGenerationClient:
    def __init__(self, config: AuthenticationConfig):
        self._url = settings["url"]
        self._headers = dict(authorizationToken=config.token)
        self._user_id = config.user_id
        self._org_id = config.org_id

    def generate(self, request: DataRequest) -> DataResponse:
        """
        Send a data generation request to Datagen's services.
        This request will trigger a data generation process that will eventually will result in an url
        link to a s3 bucket that contains the generated data.
        :param request: Data generation request that consists of all the data point requests.
        :return: Unique ID that represents the generation id of this data generation request.
        :raise InvalidRequest: In case of an invalid request.
        """
        if any(map(lambda x: not isinstance(x, HumanDatapoint), request.datapoints)):
            raise TypeError("Invalid datapoint type was provided.")
        else:
            return self._generate_human_identities_data(request=request)

    def get_status(self, generation_id: str) -> DataResponseStatus:
        """
        Data generation status consists of the following:
        1. Time estimation in ms
        2. Current generation status e.g. IN_PROGRESS, COMPLETED, FAILED, etc.
        3. Percentage of the data generation process.
        :param generation_id: Generation ID that was provided by generate_data call.
        :return: Data generation status.
        :raise: GenerationIdNotFoundError in case of an invalid generation id
        """
        response = requests.get(url=self._url + f"/generations/status/{generation_id}", headers=self._headers)
        if response.status_code != HTTPStatus.OK:
            message = f"Failed to get generation status of {generation_id}."
            HttpStatusHandler.handle(status_code=response.status_code, message=message)

        response_data = json.loads(response.content)
        return DataResponseStatus(
            estimation_time_ms=response_data["estimatedTime"],
            status=response_data["status"],
            percentage=response_data["percentage"],
        )

    def get_download_urls(self, generation_id: str) -> List[str]:
        """
        Once data generation of a generation_id is done, a download link will be provided.
        :param generation_id: Generation ID that was provided by generate_data call.
        :return: Download links to generated data.
        :raise: GenerationIdNotFoundError in case of an invalid generation id.
        :raise: InvalidRequest in case of an invalid request.
        """
        response = requests.get(url=self._url + f"delivery/{generation_id}", headers=self._headers)
        if response.status_code == HTTPStatus.ACCEPTED:
            logger.info(
                f"Data generation is in progress. Download links for generation ID {generation_id} will soon be ready."
            )
            return []

        elif response.status_code != HTTPStatus.OK:
            message = f"Failed to get s3 url for get download urls for {generation_id}."
            HttpStatusHandler.handle(status_code=response.status_code, message=message)

        logger.info(f"Successfully received download links for generation id: {generation_id}.")
        return json.loads(response.content)

    def stop(self, generation_id: str) -> None:
        """
        Stops data generation request.
        A table of all generation requests and their progress can be found here:
        https://app.prod.datagen.tech/dataset.

        :param generation_id: Generation ID that was provided by generate_data call.
        :raise: InvalidRequest in case of an invalid request.
        """
        response = requests.post(url=self._url + f"/generations/stop/{generation_id}", headers=self._headers)
        if response.status_code != HTTPStatus.OK:
            message = f"Failed to stop generation: {generation_id}."
            HttpStatusHandler.handle(status_code=response.status_code, message=message)

        logger.info(f"Successfully stopped data generation request: {generation_id}.")

    @classmethod
    def download(cls, urls: List[str], dest: Path) -> None:
        """
        Download the datasets provided by the get_download_urls method.
        Links are available for a limited time. If links are expired use get_download_urls to get valid urls.
        :param urls: Download urls received from get_download_urls method.
        :param dest: Directory to download the datasets to. If
        """
        if not dest.exists() and dest.is_dir():
            logger.error(f"Failed to download files to {str(dest)}. Directory does not exists.")
            raise FileExistsError(f"Directory {str(dest)} does not exists.")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(DataGenerationClient._download_file, url) for url in urls]

            for future in concurrent.futures.as_completed(results):
                url = urls[results.index(future)]
                try:
                    data = future.result()
                except Exception as e:
                    logger.error(f"{url} generated an exception: {e}")

                else:
                    filename = DataGenerationClient._extract_filename(url=url)
                    with open(f"{str(dest)}/{filename}", "wb") as f:
                        f.write(data)
                        logger.info(f"Successfully downloaded dataset to {str(dest)}/{filename}")

    @staticmethod
    def _download_file(url: str) -> bytes:
        response = requests.get(url)
        return response.content

    @staticmethod
    def _extract_filename(url: str) -> str:
        query = urllib.parse.urlsplit(url).query
        params = urllib.parse.parse_qs(query)
        return params["response-content-disposition"][0].split("=")[1].strip()

    def _generate_human_identities_data(self, request: DataRequest) -> DataResponse:
        params = dict(userId=self._user_id, orgId=self._org_id)
        response = requests.post(
            url=self._url + "/generations", params=params, headers=self._headers, json=request.dict()
        )
        if response.status_code != HTTPStatus.OK:
            message = f"Failed to generate a human identities data request with error: {json.loads(response.content)}"
            HttpStatusHandler.handle(status_code=response.status_code, message=message)

        logger.info("Successfully created a human identities data generation request.")
        response_info = json.loads(response.content)
        return DataResponse(
            generation_name=response_info["title"],
            renders=response_info["renders"],
            scenes=response_info["scenes"],
            generation_id=response_info["generationId"],
            dgu_hour=response_info["dguhCost"],
        )
