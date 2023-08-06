from __future__ import annotations

from pydantic import BaseModel


class TelegramAPI(BaseModel):
    api_url: str
