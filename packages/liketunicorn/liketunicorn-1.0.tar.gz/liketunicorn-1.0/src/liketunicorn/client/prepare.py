from __future__ import annotations

import datetime
import json
from enum import Enum
from typing import Any, Union


def prepare_value(value: Any) -> Union[str, int, bool]:
    if isinstance(value, str):
        return value
    if isinstance(value, (list, dict)):
        return json.dumps(clean_json(value))
    if isinstance(value, datetime.timedelta):
        now = datetime.datetime.now()
        return str(round((now + value).timestamp()))
    if isinstance(value, datetime.datetime):
        return str(round(value.timestamp()))
    if isinstance(value, Enum):
        return prepare_value(value.value)
    return str(value)


def clean_json(value: Any) -> Any:
    if isinstance(value, list):
        return [clean_json(v) for v in value if v is not None]
    if isinstance(value, dict):
        return {k: clean_json(v) for k, v in value.items() if v is not None}
    return value
