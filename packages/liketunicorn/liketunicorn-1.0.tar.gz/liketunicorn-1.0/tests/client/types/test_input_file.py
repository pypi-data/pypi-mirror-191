from __future__ import annotations

from typing import AsyncIterable, Union

import pytest

from liketunicorn.client.types import FileSystemInputFile, InputFile


@pytest.mark.asyncio
class TestInputFile:
    async def test_fs_input_file(self) -> None:
        file = FileSystemInputFile(path=__file__)

        assert isinstance(file, Union[InputFile, AsyncIterable])
        filename = file.path.split("/")[-1]
        assert filename.startswith("test_") and filename.endswith(".py")

    async def test_fs_input_file_readable(self) -> None:
        file = FileSystemInputFile(path=__file__, chunk_size=1)

        assert file.chunk_size == 1

        size = 0
        async for chunk in file:
            chunk_len = len(chunk)
            assert chunk_len == 1
            size += chunk_len

        assert size > 0
