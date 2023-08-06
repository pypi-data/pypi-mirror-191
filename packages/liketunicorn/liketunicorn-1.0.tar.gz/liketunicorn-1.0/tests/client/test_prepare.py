from __future__ import annotations

import datetime
from enum import Enum
from typing import Any

import pytest

from liketunicorn.client.prepare import clean_json, prepare_value


class EnumInt(int, Enum):
    value = 1


class EnumStr(str, Enum):
    value = "str"


@pytest.mark.parametrize(
    "to_prepare,prepared",
    [
        ("hello", "hello"),
        ([1, 2], "[1, 2]"),
        ([1, {"hello": "python"}, 3], '[1, {"hello": "python"}, 3]'),
        (
            [1, {"hello": "python", "list": [1, {"hello": "python", "list": [1, 2, 3]}]}],
            '[1, {"hello": "python", "list": [1, {"hello": "python", "list": [1, 2, 3]}]}]',
        ),
        ({"hello": "python"}, '{"hello": "python"}'),
        ({"hello": "python", "list": [1, 2]}, '{"hello": "python", "list": [1, 2]}'),
        (datetime.timedelta(minutes=2), "skip"),
        (now := datetime.datetime.now(), str(round(now.timestamp()))),
        (EnumInt.value, "1"),
        (EnumStr.value, "str"),
    ],
)
def test_prepare_value(to_prepare: Any, prepared: str) -> None:
    if isinstance(to_prepare, datetime.timedelta):
        assert isinstance(prepare_value(to_prepare), str)
    else:
        assert prepare_value(to_prepare) == prepared


@pytest.mark.parametrize(
    "to_clean,cleaned",
    [
        ({"hello": "python", "some": "value", "none": None}, {"hello": "python", "some": "value"}),
        (
            ["hello", None, "python", {"hello": "python", "none": None}],
            ["hello", "python", {"hello": "python"}],
        ),
    ],
)
def test_clean_json(to_clean: Any, cleaned: Any) -> None:
    assert clean_json(to_clean) == cleaned
