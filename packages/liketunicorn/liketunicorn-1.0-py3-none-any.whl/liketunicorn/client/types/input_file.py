from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import AsyncIterator, Optional, Union

import aiofiles

from liketunicorn.client.types.base import TelegramObject

DEFAULT_CHUNK_SIZE = 64 * 1024


class _AIterSupport:
    async def __aiter__(self) -> AsyncIterator[bytes]:
        async for chunk in self.read():  # noqa
            yield chunk


class InputFile(ABC, TelegramObject, _AIterSupport):
    chunk_size: int = DEFAULT_CHUNK_SIZE
    filename: Optional[str] = None

    @abstractmethod
    async def read(self) -> AsyncIterator[bytes, ...]:
        ...


class FileSystemInputFile(InputFile):
    path: Union[str, Path]

    async def read(self) -> AsyncIterator[bytes, ...]:
        async with aiofiles.open(self.path, "rb") as file:
            while chunk := await file.read(self.chunk_size):
                yield chunk
