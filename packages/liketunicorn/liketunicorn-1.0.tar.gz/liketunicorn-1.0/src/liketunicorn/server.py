from __future__ import annotations

import asyncio
import sys
from typing import Optional

from liketunicorn.client import SessionManager
from liketunicorn.config import Config
from liketunicorn.enums import RunTypeEnum
from liketunicorn.logger import logger
from liketunicorn.polling import polling


class Server:
    def __init__(self, config: Config, *, session: Optional[SessionManager] = None) -> None:
        self.config = config
        self.session = SessionManager(api=self.config.api_config) if session is None else session

    def run(self) -> None:  # pragma: no cover
        return asyncio.run(self.serve())

    async def serve(self) -> None:  # pragma: no cover
        if not self.config.loaded:
            self.config.load()

        await self.main_loop()

    async def main_loop(self) -> None:
        try:
            if self.config.run_type == RunTypeEnum.POLLING:
                await polling(  # pragma: no cover
                    app=self.config.loaded_app,
                    session=self.session,
                    run_config=self.config.run_config,
                )
            else:
                message = (
                    "Currently unsupported run type '{run_type}', also available: [{available}]."
                )
                raise ValueError(
                    message.format(run_type=self.config.run_type, available=list(RunTypeEnum))
                )
        except ValueError as e:
            logger.error("Error to start app: %s." % e)
            sys.exit(1)
        finally:
            await self.session.close()
