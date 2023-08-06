from __future__ import annotations

import pytest

from liketunicorn.config import Config


def test_load_failed(polling_config: Config) -> None:
    polling_config.loaded = True

    with pytest.raises(AssertionError):
        polling_config.load()


def test_load_with_importer_error(polling_config: Config) -> None:
    polling_config.app = "some:lol"

    with pytest.raises(SystemExit):
        polling_config.load()

    assert not polling_config.loaded


def test_load_no_callable(polling_config: Config) -> None:
    polling_config.app = "not_callable_app:app"

    with pytest.raises(SystemExit):
        polling_config.load()

    assert not polling_config.loaded


def test_load_successfully(polling_config: Config) -> None:
    polling_config.load()
    assert polling_config.loaded
