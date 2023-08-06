from __future__ import annotations

import pytest

from liketunicorn.exceptions import ImporterError
from liketunicorn.importer import import_from_string


@pytest.mark.parametrize(
    "to_import,excepted",
    [
        ("some:", "Import string 'some:' must be '<module>:<attribute>'"),
        (":attr", "Import string ':attr' must be '<module>:<attribute>'"),
        ("no_module:attr", "Could not to import module 'no_module'"),
        ("raise_error:attr", "Could not to import module 'raise_error'"),
    ],
)
def test_invalid_format(to_import: str, excepted: str) -> None:
    with pytest.raises(ImporterError) as exception_info:
        import_from_string(to_import)
    assert excepted in str(exception_info.value)


def test_valid_import() -> None:
    from tempfile import TemporaryFile

    instance = import_from_string("tempfile:TemporaryFile")
    assert instance == TemporaryFile


def test_no_import_needed() -> None:
    from tempfile import TemporaryFile

    instance = import_from_string(TemporaryFile)
    assert instance == TemporaryFile
