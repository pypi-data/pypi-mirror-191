import asyncio
from time import perf_counter
from typing import AsyncGenerator, Awaitable, Callable, Tuple

from liketunicorn.client import SessionManager
from liketunicorn.client.methods import GetUpdates
from liketunicorn.client.types import TelegramObject
from liketunicorn.logger import logger


async def _feed(app: Callable[..., Awaitable[None]], method: str, update: TelegramObject) -> None:
    await app(update, method=method)


async def _listen(
    session: SessionManager, config: GetUpdates
) -> AsyncGenerator[Tuple[str, TelegramObject], None]:
    SLEEP_TIME = 0.5
    logger.debug(
        "Listen updates:",
        f"on error sleep time {SLEEP_TIME}",
        "process updates timer registered",
    )

    get_updates = config
    while True:
        start = perf_counter()
        logger.debug("Start process updates")

        try:
            updates = await session.request(get_updates)
            logger.debug(f"Got new updates `updates[{len(updates)}]`")
        except Exception as e:
            logger.error("Skip updates: %s: %s." % (type(e).__name__, e))
            updates = []
            await asyncio.sleep(SLEEP_TIME)
        for update in updates:
            logger.debug(f"Process `update<{update.update_id}>`")
            yield update.type, update.update

            get_updates.offset = update.update_id + 1
        end = perf_counter()
        logger.debug(f"Successfully processed updates: time(ns) - {end - start}")


async def _polling(
    app: Callable[..., Awaitable[None]], session: SessionManager, config: GetUpdates
) -> None:
    async for method, update in _listen(session=session, config=config):
        await _feed(app=app, method=method, update=update)


async def polling(
    app: Callable[..., Awaitable[None]],
    session: SessionManager,
    run_config: str,
) -> None:
    config = GetUpdates.parse_file(run_config)
    await _polling(app=app, session=session, config=config)
