import importlib
from typing import Any

from liketunicorn.exceptions import ImporterError


def import_from_string(import_str: str) -> Any:
    module_str, _, attrs_str = import_str.partition(":")
    if not module_str or not attrs_str:
        raise ImporterError(f"Import string '{import_str}' must be '<module>:<attribute>'")

    try:
        module = importlib.import_module(module_str)
    except ImportError:
        raise ImporterError(f"Could not to import module '{module_str}'")

    instance = module
    try:
        for attr_str in attrs_str.split("."):
            instance = getattr(instance, attr_str)
    except AttributeError:
        raise ImporterError(f"Attribute '{attrs_str}' not found in module '{module_str}'")

    return instance
