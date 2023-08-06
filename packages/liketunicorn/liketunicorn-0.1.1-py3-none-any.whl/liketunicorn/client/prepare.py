from __future__ import annotations

import datetime
import json
from enum import Enum
from typing import Any, Union


def prepare_value(value: Any) -> Union[str, int, bool]:
    if isinstance(value, str):
        return value
    if isinstance(value, (list, dict)):
        return json.dumps(_clean_json(value))
    if isinstance(value, datetime.timedelta):
        now = datetime.datetime.now()
        return str(round((now + value).timestamp()))
    if isinstance(value, datetime.datetime):
        return str(round(value.timestamp()))
    if isinstance(value, Enum):
        return value(value.value)  # noqa
    return str(value)


def _clean_json(value: Any) -> Any:  # noqa
    if isinstance(value, list):
        return [_clean_json(v) for v in value if v is not None]
    if isinstance(value, dict):
        return {k: _clean_json(v) for k, v in value.items() if v is not None}
    return value
