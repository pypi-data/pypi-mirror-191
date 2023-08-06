from argparse import ArgumentParser

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
        api_config=args.api_config,
        run_config=args.run_config,
    )


def run(
    app: str,
    *,
    run_type: RunTypeEnum,
    api_config: str,
    run_config: str,
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
    main()  # pragma: no cover
