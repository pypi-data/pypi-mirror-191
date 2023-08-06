import base64
import os

from dependency_injector import containers, providers

from datagen.api.client.impl import AuthenticationConfig, DataGenerationClient
from datagen.api.impl import DatagenAPI
from datagen.dev.logging import get_logger

logger = get_logger(__name__)


def token_setup_instructions() -> str:
    if os.name == "nt":  # Windows
        return "set DG_AUTH_TOKEN=<your-auth-token>"
    else:  # Linux and MacOS
        return "export DG_AUTH_TOKEN=<your-auth-token>"


def build_config() -> AuthenticationConfig:
    token = os.environ["DG_AUTH_TOKEN"]
    if not token:
        logger.error(
            f"Authentication token is uninitialized. You can create a new token at "
            f"https://app.prod.datagen.tech/token. After creating the token insert the following:"
            f" {token_setup_instructions()}"
        )
        raise Exception("Authentication token is uninitialized.")
    _, token_id = base64.b64decode(token).decode("utf-8").split(".")[:2]
    user_id, org_id = tuple(base64.b64decode(token_id).decode("utf-8").split(".")[:2])

    return AuthenticationConfig(token=token, user_id=user_id, org_id=org_id)


class ApiContainer(containers.DeclarativeContainer):

    config = providers.Callable(build_config)

    client = providers.Singleton(DataGenerationClient, config=config)

    api = providers.Singleton(
        DatagenAPI,
        # client=client,
    )
