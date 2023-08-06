from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Extra

from liketunicorn.mixins import ModelExcludesNoneMixin


class TelegramObject(ModelExcludesNoneMixin, BaseModel):
    class Config:
        use_enum_values = True
        extra = Extra.allow
        validate_assignment = True
        allow_mutation = False
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda dt: int(dt.timestamp())}
