from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from liketunicorn.client.methods import TelegramMethod, TelegramType


class TunicornError(Exception):
    ...


class ImporterError(TunicornError):
    ...


class DecodeError(TunicornError):
    ...


class TelegramAPIError(TunicornError):
    def __init__(self, method: TelegramMethod[TelegramType], description: str) -> None:
        super(TunicornError, self).__init__()

        self.method = method
        self.description = description


class TelegramNetworkError(TelegramAPIError):
    ...


class TelegramRetryAfter(TelegramAPIError):
    def __init__(
        self, method: TelegramMethod[TelegramType], description: str, retry_after: int
    ) -> None:
        super(TelegramRetryAfter, self).__init__(method=method, description=description)

        self.retry_after = retry_after


class TelegramMigrateToChat(TelegramAPIError):
    def __init__(
        self,
        method: TelegramMethod[TelegramType],
        description: str,
        migrate_to_chat_id: int,
    ) -> None:
        super(TelegramMigrateToChat, self).__init__(method=method, description=description)

        self.migrate_to_chat_id = migrate_to_chat_id


class TelegramBadRequest(TelegramAPIError):
    ...


class TelegramNotFound(TelegramAPIError):
    ...


class TelegramConflictError(TelegramAPIError):
    ...


class TelegramUnauthorizedError(TelegramAPIError):
    ...


class TelegramForbiddenError(TelegramAPIError):
    ...


class TelegramServerError(TelegramAPIError):
    ...


class RestartingTelegram(TelegramServerError):
    ...


class TelegramEntityTooLarge(TelegramNetworkError):
    ...
