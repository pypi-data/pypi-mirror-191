import asyncio
import sys

from liketunicorn.client import SessionManager
from liketunicorn.config import Config
from liketunicorn.enums import RunTypeEnum
from liketunicorn.logger import logger
from liketunicorn.polling import polling


class Server:
    def __init__(self, config: Config) -> None:
        self.config = config

    def run(self) -> None:
        return asyncio.run(self.serve())

    async def serve(self) -> None:
        if not self.config.loaded:
            self.config.load()

        await self.main_loop()

    async def main_loop(self) -> None:
        session = SessionManager(api=self.config.api_config)
        run_table = {RunTypeEnum.POLLING: polling}
        try:
            await run_table[self.config.run_type](
                app=self.config.loaded_app, session=session, run_config=self.config.run_config
            )
        except KeyError:
            logger.error(
                "Error to start app: %s." % f"Could not to find '{self.config.run_type}' method"
            )
            sys.exit(1)
        finally:
            await session.close()
