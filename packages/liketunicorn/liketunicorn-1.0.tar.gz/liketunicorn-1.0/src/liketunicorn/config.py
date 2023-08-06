from __future__ import annotations

import sys
from typing import Awaitable, Callable, Union

from liketunicorn.api import TelegramAPI
from liketunicorn.client.types import TelegramObject
from liketunicorn.enums import RunTypeEnum
from liketunicorn.exceptions import ImporterError
from liketunicorn.importer import import_from_string
from liketunicorn.logger import logger


class Config:
    def __init__(
        self,
        app: Union[str, Callable[..., Awaitable[None]]],
        *,
        run_type: RunTypeEnum,
        api_config: TelegramAPI,
        run_config: TelegramObject,
    ) -> None:
        self.app = app
        self.run_type = run_type
        self.api_config = api_config
        self.run_config = run_config
        self.loaded = False

    def load(self) -> None:
        assert not self.loaded

        try:
            self.loaded_app = import_from_string(self.app)
        except ImporterError as exception:
            logger.error("Error loading app: %s." % exception)
            sys.exit(1)
        if not isinstance(self.loaded_app, Callable):
            logger.error("Error loading app: %s." % "app must be callable")
            sys.exit(1)

        self.loaded = True
