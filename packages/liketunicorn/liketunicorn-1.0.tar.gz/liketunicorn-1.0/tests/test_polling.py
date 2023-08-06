from __future__ import annotations

import pytest
from pydantic.config import BaseConfig

from liketunicorn.client.methods import GetUpdates
from liketunicorn.client.types import TelegramObject, Update
from liketunicorn.polling import feed, listen
from liketunicorn.server import Server


class MutableObject(TelegramObject):
    class Config(BaseConfig):
        allow_mutation = True


@pytest.mark.asyncio
async def test_feed() -> None:
    is_called = False

    async def app(update: MutableObject) -> None:
        nonlocal is_called
        is_called = True

        update.id = 2

    _update = MutableObject(id=1)
    await feed(app, _update)

    assert is_called
    assert _update.id == 2


@pytest.mark.asyncio
async def test_listen(polling_server: Server) -> None:
    polling_server.session.mock.add_result_for(
        GetUpdates,
        ok=True,
        result=[
            Update(update_id=1),
            Update(update_id=2),
            Update(update_id=3),
            Update(update_id=0),
        ],
    )
    get_updates = GetUpdates()
    async for update in listen(session=polling_server.session, config=get_updates):
        last_known_id = update.update_id
        assert last_known_id == update.update_id
