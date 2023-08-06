from __future__ import annotations

from typing import Type

import pytest as pytest

from liketunicorn.client.client import SessionManager
from liketunicorn.client.methods import GetUpdates
from liketunicorn.client.types import TelegramObject
from liketunicorn.exceptions import (
    DecodeError,
    RestartingTelegram,
    TelegramAPIError,
    TelegramBadRequest,
    TelegramConflictError,
    TelegramEntityTooLarge,
    TelegramForbiddenError,
    TelegramMigrateToChat,
    TelegramNotFound,
    TelegramRetryAfter,
    TelegramServerError,
    TelegramUnauthorizedError,
)


@pytest.mark.parametrize(
    "status_code,content,error",
    [
        (200, '{"ok":true,"result":[]}', None),
        (400, '{"ok":false,"description":"test"}', TelegramBadRequest),
        (
            400,
            '{"ok":false,"description":"test", "parameters": {"retry_after": 1}}',
            TelegramRetryAfter,
        ),
        (
            400,
            '{"ok":false,"description":"test", "parameters": {"migrate_to_chat_id": -42}}',
            TelegramMigrateToChat,
        ),
        (404, '{"ok":false,"description":"test"}', TelegramNotFound),
        (401, '{"ok":false,"description":"test"}', TelegramUnauthorizedError),
        (403, '{"ok":false,"description":"test"}', TelegramForbiddenError),
        (409, '{"ok":false,"description":"test"}', TelegramConflictError),
        (413, '{"ok":false,"description":"test"}', TelegramEntityTooLarge),
        (500, '{"ok":false,"description":"restarting"}', RestartingTelegram),
        (500, '{"ok":false,"description":"test"}', TelegramServerError),
        (502, '{"ok":false,"description":"test"}', TelegramServerError),
        (499, '{"ok":false,"description":"test"}', TelegramAPIError),
        (499, '{"ok":false,"description":"test"}', TelegramAPIError),
        (200, '{"this": "is_not_a_valid_json', DecodeError),
        (201, '{"ok": "ok"}', DecodeError),
    ],
)
def test_check_response(status_code: int, content: str, error: Type[Exception]) -> None:
    session = SessionManager(api=TelegramObject())
    method = GetUpdates()
    if error is None:
        session.check_response(
            method=method,
            status_code=status_code,
            content=content,
        )
    else:
        with pytest.raises(error):
            session.check_response(
                method=method,
                status_code=status_code,
                content=content,
            )
