from __future__ import annotations

from typing import Optional, cast

from liketunicorn.client.types import TelegramObject
from liketunicorn.enums import UpdateType


class Update(TelegramObject):
    update_id: int
    message: Optional[TelegramObject] = None
    edited_message: Optional[TelegramObject] = None
    channel_post: Optional[TelegramObject] = None
    edited_channel_post: Optional[TelegramObject] = None
    inline_query: Optional[TelegramObject] = None
    chosen_inline_result: Optional[TelegramObject] = None
    callback_query: Optional[TelegramObject] = None
    shipping_query: Optional[TelegramObject] = None
    pre_checkout_query: Optional[TelegramObject] = None
    poll: Optional[TelegramObject] = None
    poll_answer: Optional[TelegramObject] = None
    my_chat_member: Optional[TelegramObject] = None
    chat_member: Optional[TelegramObject] = None
    chat_join_request: Optional[TelegramObject] = None

    def __hash__(self) -> int:
        return hash((type(self), self.update_id))

    @property
    def type(self) -> str:
        if self.message:
            return UpdateType.MESSAGE
        if self.edited_message:
            return UpdateType.EDITED_MESSAGE
        if self.channel_post:
            return UpdateType.CHANNEL_POST
        if self.edited_channel_post:
            return UpdateType.EDITED_CHANNEL_POST
        if self.inline_query:
            return UpdateType.INLINE_QUERY
        if self.chosen_inline_result:
            return UpdateType.CHOSEN_INLINE_RESULT
        if self.callback_query:
            return UpdateType.CALLBACK_QUERY
        if self.shipping_query:
            return UpdateType.SHIPPING_QUERY
        if self.pre_checkout_query:
            return UpdateType.PRE_CHECKOUT_QUERY
        if self.poll:
            return UpdateType.POLL
        if self.poll_answer:
            return UpdateType.POLL_ANSWER
        if self.my_chat_member:
            return UpdateType.MY_CHAT_MEMBER
        if self.chat_member:
            return UpdateType.CHAT_MEMBER
        if self.chat_join_request:
            return UpdateType.CHAT_JOIN_REQUEST
        return UpdateType.UNKNOWN

    @property
    def update(self) -> TelegramObject:
        _type = self.type
        return cast(TelegramObject, getattr(self, _type))
