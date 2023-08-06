from __future__ import annotations

from typing import Any, Awaitable, Callable

import pytest

from liketunicorn.api import TelegramAPI
from liketunicorn.client.types import TelegramObject
from liketunicorn.config import Config
from liketunicorn.enums import RunTypeEnum
from liketunicorn.server import Server
from tests.mocked_session import MockedSessionManager


@pytest.fixture
def app() -> Callable[..., Awaitable[Any]]:
    async def my_app(*args: Any, **kwargs: Any) -> None:
        return None

    yield my_app


@pytest.fixture
def api_config() -> TelegramAPI:
    api_url = "https://url.com"
    return TelegramAPI(api_url=api_url)


@pytest.fixture
def polling_run_config() -> TelegramObject:
    return TelegramObject()


@pytest.fixture
def polling_config(
    app: Callable[..., Awaitable[Any]],
    api_config: TelegramAPI,
    polling_run_config: TelegramObject,
) -> Config:
    _config = Config(
        app=app,
        run_type=RunTypeEnum.POLLING,
        api_config=api_config,
        run_config=polling_run_config,
    )

    yield _config


@pytest.fixture
def mocked_session_manager(api_config: TelegramAPI) -> MockedSessionManager:
    _mocked_session_manager = MockedSessionManager(api=api_config)
    yield _mocked_session_manager


@pytest.fixture
def polling_server(polling_config: Config, mocked_session_manager: MockedSessionManager) -> Server:
    _server = Server(config=polling_config, session=mocked_session_manager)
    yield _server


@pytest.fixture
def polling_server_without_main_loop(polling_server: Server) -> Server:
    async def plug(*args: Any, **kwargs: Any) -> None:
        ...

    polling_server.main_loop = plug
    yield polling_server
