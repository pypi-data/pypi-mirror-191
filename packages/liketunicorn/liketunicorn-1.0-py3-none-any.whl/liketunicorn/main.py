from __future__ import annotations

from argparse import ArgumentParser
from typing import Awaitable, Callable, Union

from liketunicorn.api import TelegramAPI
from liketunicorn.client.types import TelegramObject
from liketunicorn.config import Config
from liketunicorn.enums import RunTypeEnum
from liketunicorn.server import Server

parser = ArgumentParser(prog="tunicorn")
parser.add_argument("app")
parser.add_argument(
    "-rt",
    "--run-type",
    type=RunTypeEnum,
    default=RunTypeEnum.POLLING,
)
parser.add_argument(
    "-ac",
    "--api-config",
    type=str,
)
parser.add_argument(
    "-rc",
    "--run-config",
    type=str,
)


def main() -> None:
    args = parser.parse_args()
    run(
        args.app,
        run_type=args.run_type,
        api_config=TelegramAPI.parse_file(args.api_config),
        run_config=TelegramObject.parse_file(args.run_config),
    )


def run(
    app: Union[str, Callable[..., Awaitable[None]]],
    *,
    run_type: RunTypeEnum,
    api_config: TelegramAPI,
    run_config: TelegramObject,
) -> None:
    config = Config(
        app,
        run_type=run_type,
        api_config=api_config,
        run_config=run_config,
    )
    server = Server(config=config)

    server.run()


if __name__ == "__main__":
    main()
