from __future__ import annotations

from typing import Any, Dict, Optional

import pytest
from pydantic import BaseModel

from liketunicorn.mixins import ModelExcludesNoneMixin


class MyModel(ModelExcludesNoneMixin, BaseModel):
    value: Optional[int] = None
    another_value: Optional[str] = None


@pytest.mark.parametrize(
    "model,result",
    [
        (MyModel(value=1), '{"value": 1}'),
        (MyModel(another_value="hello"), '{"another_value": "hello"}'),
        (MyModel(value=1, another_value="hello"), '{"value": 1, "another_value": "hello"}'),
        (MyModel(), "{}"),
    ],
)
def test_model_excludes_none_mixin_json(model: MyModel, result: str) -> None:
    assert model.json() == result


@pytest.mark.parametrize(
    "model,result",
    [
        (MyModel(value=1), {"value": 1}),
        (MyModel(another_value="hello"), {"another_value": "hello"}),
        (MyModel(value=1, another_value="hello"), {"value": 1, "another_value": "hello"}),
        (MyModel(), {}),
    ],
)
def test_model_excludes_none_mixin_dict(model: MyModel, result: Dict[str, Any]) -> None:
    assert model.dict() == result
