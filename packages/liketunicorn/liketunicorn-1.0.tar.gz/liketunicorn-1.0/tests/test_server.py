from __future__ import annotations

import pytest

from liketunicorn.server import Server


def test_serve_with_loaded_config(polling_server_without_main_loop: Server) -> None:
    config = polling_server_without_main_loop.config
    config.load()

    polling_server_without_main_loop.run()
    assert config.loaded


def test_serve_with_non_loaded_config(polling_server_without_main_loop: Server) -> None:
    config = polling_server_without_main_loop.config

    polling_server_without_main_loop.run()
    assert config.loaded


def test_serve_with_not_available_method(polling_server: Server) -> None:
    config = polling_server.config
    config.run_type = "unsupported"

    with pytest.raises(SystemExit):
        polling_server.run()

    assert config.loaded


@pytest.mark.asyncio
async def test_main_loop(polling_server: Server) -> None:
    config = polling_server.config
    config.run_type = "unavailable"
    config.load()

    with pytest.raises(SystemExit):
        await polling_server.main_loop()
