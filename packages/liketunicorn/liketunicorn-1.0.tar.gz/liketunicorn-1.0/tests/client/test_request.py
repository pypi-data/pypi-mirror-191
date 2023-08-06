from __future__ import annotations

import asyncio
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from aiohttp import ClientError
from aresponses import ResponsesMockServer

from liketunicorn.api import TelegramAPI
from liketunicorn.client import SessionManager
from liketunicorn.client.methods import (
    GetUpdates,
    Request,
    TelegramMethod,
    TelegramType,
)
from liketunicorn.client.types import TelegramObject
from liketunicorn.exceptions import TelegramNetworkError


class CustomSession(SessionManager):
    async def create(self) -> None:
        ...

    async def close(self) -> None:
        ...

    async def request(
        self, method: TelegramMethod[TelegramType], timeout: int = 60.0
    ) -> None:  # type: ignore
        assert isinstance(method, TelegramMethod)


@pytest.mark.asyncio
async def test_make_request_simple() -> None:
    session = CustomSession(api=TelegramObject())

    assert await session.request(GetUpdates()) is None


@pytest.mark.asyncio
async def test_make_request_with_aresponses(aresponses: ResponsesMockServer) -> None:
    aresponses.add(
        aresponses.ANY,
        "/bot42:TEST/method",
        "post",
        aresponses.Response(
            status=200,
            text='{"ok": true, "result": 42}',
            headers={"Content-Type": "application/json"},
        ),
    )

    session = SessionManager(api=TelegramAPI(api_url="https://telegram.org/bot42:TEST/{method}"))

    class TestMethod(TelegramMethod[int]):
        __returns__ = int

        def request(self) -> Request:
            return Request(method="method", data={})

    call = TestMethod()

    result = await session.request(call)
    assert isinstance(result, int)
    assert result == 42


@pytest.mark.asyncio
@pytest.mark.parametrize("error", [ClientError("mocked"), asyncio.TimeoutError()])
async def test_make_request_network_error(error) -> None:
    session = SessionManager(api=TelegramAPI(api_url="https://telegram.org/bot42:TEST/{method}"))

    async def side_effect(*args: Any, **kwargs: Any) -> None:
        raise error

    with patch(
        "aiohttp.client.ClientSession._request",
        new_callable=AsyncMock,
        side_effect=side_effect,
    ):
        with pytest.raises(TelegramNetworkError):
            await session.request(GetUpdates())
