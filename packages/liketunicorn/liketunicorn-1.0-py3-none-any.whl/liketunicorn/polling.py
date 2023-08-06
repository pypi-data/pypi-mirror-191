from __future__ import annotations

import asyncio
from time import perf_counter
from typing import AsyncGenerator, Awaitable, Callable

from liketunicorn.client import SessionManager
from liketunicorn.client.methods import GetUpdates
from liketunicorn.client.types import TelegramObject, Update
from liketunicorn.logger import logger


async def feed(app: Callable[..., Awaitable[None]], update: TelegramObject) -> None:
    await app(update)


async def listen(session: SessionManager, config: GetUpdates) -> AsyncGenerator[Update, None]:
    SLEEP_TIME = 0.5
    logger.info(
        "Listen updates:",
        f"on error sleep time {SLEEP_TIME}",
        "process updates timer registered",
        "rule to close: Update.update_id must be 0",
    )
    need_to_close = False

    get_updates = config
    while not need_to_close:
        start = perf_counter()
        logger.debug("Start process updates")

        try:
            updates = await session.request(get_updates)
            logger.debug(f"Got new updates `updates[{len(updates)}]`")
        except Exception as e:  # pragma: no cover
            logger.error("Skip updates: %s: %s." % (type(e).__name__, e))
            updates = []
            await asyncio.sleep(SLEEP_TIME)
        for update in updates:
            if not update.update_id:
                logger.info("Got none update, it's call to close listen, process last updates")
                need_to_close = True
            logger.debug(f"Process `update<{update.update_id}>`")
            yield update

            get_updates.offset = update.update_id + 1
        end = perf_counter()
        logger.debug(f"Successfully processed updates: time(ns) - {end - start}")

    logger.info("Listen closed")


async def _polling(
    app: Callable[..., Awaitable[None]], session: SessionManager, config: GetUpdates
) -> None:  # pragma: no cover
    async for update in listen(session=session, config=config):
        await feed(app=app, update=update)


async def polling(
    app: Callable[..., Awaitable[None]],
    session: SessionManager,
    run_config: TelegramObject,
) -> None:  # pragma: no cover
    config = GetUpdates.parse_obj(run_config)
    await _polling(app=app, session=session, config=config)
