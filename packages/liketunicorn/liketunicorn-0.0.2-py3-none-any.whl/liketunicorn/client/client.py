from __future__ import annotations

import asyncio
import json
from http import HTTPStatus
from typing import Final, Optional, cast

from aiohttp import ClientError, ClientSession, FormData
from pydantic import ValidationError

from liketunicorn.api import TelegramAPI
from liketunicorn.client.methods import Request, Response, TelegramMethod, TelegramType
from liketunicorn.client.prepare import prepare_value
from liketunicorn.exceptions import (
    DecodeError,
    RestartingTelegram,
    TelegramAPIError,
    TelegramBadRequest,
    TelegramConflictError,
    TelegramEntityTooLarge,
    TelegramForbiddenError,
    TelegramMigrateToChat,
    TelegramNetworkError,
    TelegramNotFound,
    TelegramRetryAfter,
    TelegramServerError,
    TelegramUnauthorizedError,
)


class _SessionManager:
    def __init__(self, *, session: Optional[ClientSession] = None) -> None:
        self._session: Optional[ClientSession] = None if session is None else session
        self._should_reset_session = True if self._session is None else False

    async def create(self) -> None:
        if self._should_reset_session:
            await self.close()
        if self._session is None or self._session.closed:
            self._session = ClientSession()
            self._should_reset_session = False

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()


_REQUEST_TIMEOUT: Final[int] = 60


class _SessionRequestManager(_SessionManager):
    def __init__(
        self,
        *,
        api: TelegramAPI,
        session: Optional[ClientSession] = None,
    ) -> None:
        super(_SessionRequestManager, self).__init__(session=session)

        self.api = api

    def _build_data(self, request: Request) -> FormData:  # noqa
        form = FormData(quote_fields=False)
        for key, value in request.data.items():
            form.add_field(key, prepare_value(value))
        if request.files:
            for key, value in request.files.items():
                form.add_field(key, value, filename=value.filename or key)
        return form

    def check_response(  # noqa
        self, method: TelegramMethod[TelegramType], status_code: int, content: str
    ) -> Response[TelegramType]:
        try:
            json_data = json.loads(content)
        except Exception as e:
            raise DecodeError("Failed to decode object", e, content)

        try:
            response = method.response(json_data)
        except ValidationError as e:
            raise DecodeError("Failed to deserialize object", e, json_data)

        if HTTPStatus.OK <= status_code <= HTTPStatus.IM_USED and response.ok:
            return response

        description = cast(str, response.description)

        if parameters := response.parameters:
            if parameters.retry_after:
                raise TelegramRetryAfter(
                    method=method, description=description, retry_after=parameters.retry_after
                )
            if parameters.migrate_to_chat_id:
                raise TelegramMigrateToChat(
                    method=method,
                    description=description,
                    migrate_to_chat_id=parameters.migrate_to_chat_id,
                )
        if status_code == HTTPStatus.BAD_REQUEST:
            raise TelegramBadRequest(method=method, description=description)
        if status_code == HTTPStatus.NOT_FOUND:
            raise TelegramNotFound(method=method, description=description)
        if status_code == HTTPStatus.CONFLICT:
            raise TelegramConflictError(method=method, description=description)
        if status_code == HTTPStatus.UNAUTHORIZED:
            raise TelegramUnauthorizedError(method=method, description=description)
        if status_code == HTTPStatus.FORBIDDEN:
            raise TelegramForbiddenError(method=method, description=description)
        if status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE:
            raise TelegramEntityTooLarge(method=method, description=description)
        if status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
            if "restart" in description:
                raise RestartingTelegram(method=method, description=description)
            raise TelegramServerError(method=method, description=description)

        raise TelegramAPIError(
            method=method,
            description=description,
        )

    async def request(
        self, method: TelegramMethod[TelegramType], timeout: int = _REQUEST_TIMEOUT
    ) -> TelegramType:
        await self.create()

        request = method.request()
        url = self.api.api_url.format(method=request.method)
        data = self._build_data(request)

        try:
            async with self._session.post(url, data=data, timeout=timeout) as response:
                content = await response.text()
        except asyncio.TimeoutError:
            raise TelegramNetworkError(method=method, description="request timeout error")
        except ClientError as e:
            raise TelegramNetworkError(method=method, description=f"{type(e).__name__}: {e}")
        response = self.check_response(method=method, status_code=response.status, content=content)
        return cast(TelegramType, response.result)


class SessionManager:
    def __init__(
        self,
        *,
        api: TelegramAPI,
        session: Optional[ClientSession] = None,
    ) -> None:
        self._session_request_manager = _SessionRequestManager(api=api, session=session)

    async def close(self) -> None:
        await self._session_request_manager.close()

    async def request(
        self, method: TelegramMethod[TelegramType], timeout: int = _REQUEST_TIMEOUT
    ) -> TelegramType:
        response = await self._session_request_manager.request(method=method, timeout=timeout)
        return cast(TelegramType, response)
