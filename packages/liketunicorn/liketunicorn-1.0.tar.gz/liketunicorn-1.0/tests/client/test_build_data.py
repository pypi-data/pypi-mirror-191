from __future__ import annotations

from liketunicorn.client.client import SessionManager
from liketunicorn.client.methods import Request
from liketunicorn.client.types import FileSystemInputFile, TelegramObject


def test_build_form_data_with_data_only() -> None:
    request = Request(
        method="method",
        data={
            "str": "value",
            "int": 42,
            "bool": True,
            "null": None,
            "list": ["foo"],
            "dict": {"hello": "python"},
        },
    )

    session = SessionManager(api=TelegramObject())
    form = session.build_data(request)

    fields = form._fields
    assert len(fields) == 5
    assert all(isinstance(field[2], str) for field in fields)
    assert "null" not in [item[0]["name"] for item in fields]


def test_build_form_data_with_files() -> None:
    request = Request(
        method="method",
        data={"key": "value"},
        files={"document": FileSystemInputFile(path=__file__, filename="hello.py")},
    )

    session = SessionManager(api=TelegramObject())
    form = session.build_data(request)

    fields = form._fields

    assert len(fields) == 2
    assert fields[1][0]["name"] == "document"
    assert fields[1][0]["filename"] == "hello.py"
    assert isinstance(fields[1][2], FileSystemInputFile)
