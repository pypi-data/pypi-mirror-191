class LikeTunicornError(Exception):
    ...


class ImporterError(LikeTunicornError):
    ...


class DecodeError(LikeTunicornError):
    ...


class TelegramAPIError(LikeTunicornError):
    ...


class TelegramNetworkError(TelegramAPIError):
    ...


class TelegramRetryAfter(TelegramAPIError):
    ...


class TelegramMigrateToChat(TelegramAPIError):
    ...


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
