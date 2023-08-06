from __future__ import annotations

import pytest

from liketunicorn.client.client import SessionManager
from liketunicorn.client.types import TelegramObject


class ClientSession:
    closed: bool = True

    def __init__(self) -> None:
        self.closed = False

    async def close(self) -> None:
        self.closed = True


@pytest.mark.asyncio
async def test_session_close_session() -> None:
    session = SessionManager(api=TelegramObject(), session=ClientSession())

    await session.close()
    assert session._session.closed


@pytest.mark.asyncio
async def test_session_close_without_session() -> None:
    session = SessionManager(api=TelegramObject())

    await session.close()
    assert session._session is None


@pytest.mark.asyncio
async def test_create_session_with_should_reset() -> None:
    session = SessionManager(api=TelegramObject())

    assert session._should_reset_session and session._session is None
    await session.create()

    assert not session._should_reset_session


@pytest.mark.asyncio
async def test_create_session_without_should_reset() -> None:
    session = SessionManager(api=TelegramObject(), session=ClientSession())
    assert not session._should_reset_session
    await session.create()
    assert session._session and not session._session.closed
