from typing import Optional

from .base import TelegramObject
from .input_file import FileSystemInputFile, InputFile
from .response_parameters import ResponseParameters
from .update import Update

__all__ = (
    "TelegramObject",
    "InputFile",
    "FileSystemInputFile",
    "ResponseParameters",
    "Update",
)

for _entity_name in __all__:
    _entity = globals()[_entity_name]
    if not hasattr(_entity, "update_forward_refs"):
        continue
    _entity.update_forward_refs(
        **{k: v for k, v in globals().items() if k in __all__},
        **{"Optional": Optional},
    )

del _entity
del _entity_name
