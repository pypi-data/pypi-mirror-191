from __future__ import annotations

import abc
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseConfig, BaseModel, Extra
from pydantic.generics import GenericModel

from liketunicorn.client.types import InputFile, ResponseParameters
from liketunicorn.mixins import ModelExcludesNoneMixin

TelegramType = TypeVar("TelegramType", bound=Any)


class Request(BaseModel, ModelExcludesNoneMixin):
    method: str

    data: Dict[str, Any]
    files: Optional[Dict[str, InputFile]]

    class Config(BaseConfig):
        arbitrary_types_allowed = True


class Response(ModelExcludesNoneMixin, GenericModel, Generic[TelegramType]):
    ok: bool
    result: Optional[TelegramType] = None
    description: Optional[str] = None
    error_code: Optional[int] = None
    parameters: Optional[ResponseParameters] = None


class TelegramMethod(ABC, ModelExcludesNoneMixin, BaseModel, Generic[TelegramType]):
    class Config(BaseConfig):
        extra = Extra.allow
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        smart_union = True

    @property
    @abc.abstractmethod
    def __returns__(self) -> ...:  # pragma: no cover
        ...

    @abstractmethod
    def request(self) -> Request:  # pragma: no cover
        ...

    def response(self, data: Dict[str, Any]) -> Response[TelegramType]:  # pragma: no cover
        return Response[self.__returns__].parse_obj(data)
