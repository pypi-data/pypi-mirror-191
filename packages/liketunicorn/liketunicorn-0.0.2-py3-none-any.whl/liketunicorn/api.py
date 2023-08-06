from pydantic import BaseModel


class TelegramAPI(BaseModel):
    api_url: str
