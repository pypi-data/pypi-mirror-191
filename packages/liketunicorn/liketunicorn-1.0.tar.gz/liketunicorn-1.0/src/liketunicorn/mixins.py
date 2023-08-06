from __future__ import annotations

from typing import AbstractSet, Any, Callable, Dict, Mapping, Optional, Union


class ModelExcludesNoneMixin:
    def dict(
        self,
        *,
        include: Optional[
            Union[
                AbstractSet[Union[int, str]],
                Mapping[Union[int, str], Any],
            ]
        ] = None,
        exclude: Optional[
            Union[
                AbstractSet[Union[int, str]],
                Mapping[Union[int, str], Any],
            ]
        ] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> Dict[str, Any]:
        exclude_none = True

        return super(ModelExcludesNoneMixin, self).dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )

    def json(
        self,
        *,
        include: Optional[
            Union[
                AbstractSet[Union[int, str]],
                Mapping[Union[int, str], Any],
            ]
        ] = None,
        exclude: Optional[
            Union[
                AbstractSet[Union[int, str]],
                Mapping[Union[int, str], Any],
            ]
        ] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        encoder: Optional[Callable[[Any], Any]] = None,
        models_as_dict: bool = True,
        **dumps_kwargs: Any,
    ) -> str:
        exclude_none = True

        return super(ModelExcludesNoneMixin, self).json(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            encoder=encoder,
            models_as_dict=models_as_dict,
            **dumps_kwargs,
        )
