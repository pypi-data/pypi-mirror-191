from __future__ import annotations

from typing import Any, Dict, List, Optional

from liketunicorn.client.methods.base import Request, TelegramMethod
from liketunicorn.client.types import Update


class GetUpdates(TelegramMethod[List[Update]]):
    __returns__ = List[Update]

    offset: Optional[int] = None
    limit: Optional[int] = None
    timeout: Optional[int] = None
    allowed_updates: Optional[List[str]] = None

    def request(self) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="getUpdates", data=data)
