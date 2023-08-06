from __future__ import annotations

import pytest

from liketunicorn.client.types import TelegramObject, Update
from liketunicorn.enums import UpdateType


@pytest.mark.parametrize(
    "attr,enum",
    [
        ("message", UpdateType.MESSAGE),
        ("edited_message", UpdateType.EDITED_MESSAGE),
        ("channel_post", UpdateType.CHANNEL_POST),
        ("edited_channel_post", UpdateType.EDITED_CHANNEL_POST),
        ("inline_query", UpdateType.INLINE_QUERY),
        ("chosen_inline_result", UpdateType.CHOSEN_INLINE_RESULT),
        ("callback_query", UpdateType.CALLBACK_QUERY),
        ("shipping_query", UpdateType.SHIPPING_QUERY),
        ("pre_checkout_query", UpdateType.PRE_CHECKOUT_QUERY),
        ("poll", UpdateType.POLL),
        ("poll_answer", UpdateType.POLL_ANSWER),
        ("my_chat_member", UpdateType.MY_CHAT_MEMBER),
        ("chat_member", UpdateType.CHAT_MEMBER),
        ("chat_join_request", UpdateType.CHAT_JOIN_REQUEST),
        ("unknown", UpdateType.UNKNOWN),
    ],
)
def test_update_type(attr: str, enum: UpdateType) -> None:
    update = Update(update_id=1, **{attr: TelegramObject()})
    assert update.type == enum


@pytest.mark.parametrize(
    "attr,o",
    [
        ("message", TelegramObject(id=1)),
        ("edited_message", TelegramObject(id=1)),
    ],
)
def test_get_update(attr: str, o: TelegramObject) -> None:
    update = Update(update_id=1, **{attr: o})
    _o = update.update

    assert _o == o


def test_update_hash() -> None:
    update1 = Update(update_id=1)
    update2 = Update(update_id=2)

    assert hash(update1) != hash(update2)
