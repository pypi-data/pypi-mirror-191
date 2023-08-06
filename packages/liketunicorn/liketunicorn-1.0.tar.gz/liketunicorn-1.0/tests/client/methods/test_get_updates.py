from __future__ import annotations

import pytest

from liketunicorn.client.methods import GetUpdates
from liketunicorn.client.types import Update
from liketunicorn.server import Server


@pytest.mark.asyncio
class TestGetUpdates:
    async def test_method(self, polling_server: Server) -> None:
        result = polling_server.session.mock.add_result_for(
            GetUpdates, ok=True, result=[Update(update_id=1)]
        )
        response = await polling_server.session.request(GetUpdates())
        request = polling_server.session.mock.get_request()

        assert request.method == "getUpdates"
        assert response == result.result
