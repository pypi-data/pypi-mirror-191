from http import HTTPStatus

from datagen.dev.logging import get_logger

logger = get_logger(__name__)


class ClientException(Exception):
    message = ""

    def __init__(self, response_msg: str, generation_id: str = None):
        self.msg = self.message.format(response_msg=response_msg, generation_id=generation_id)


class InvalidRequest(ClientException):
    message = "Invalid request error. Failed with error: {response_msg}"


class AuthenticationError(ClientException):
    message = "Authentication error. Authentication token is invalid or expired." " Failed with error: {response_msg}"


class GenerationIdNotFoundError(ClientException):
    message = "Generation ID: {generation_id} not found error. Failed with error: {response_msg}"


class HttpStatusHandler:
    status_exception_map = {
        HTTPStatus.FORBIDDEN: AuthenticationError,
        HTTPStatus.NOT_FOUND: GenerationIdNotFoundError,
        HTTPStatus.INTERNAL_SERVER_ERROR: InvalidRequest,
    }

    @classmethod
    def handle(cls, status_code: int, message: str = None) -> None:
        exception_class = cls.status_exception_map.get(status_code)
        if exception_class:
            logger.error(message)
            raise exception_class(message)
        else:
            raise ClientException("Something when wrong. Please try again later.")
