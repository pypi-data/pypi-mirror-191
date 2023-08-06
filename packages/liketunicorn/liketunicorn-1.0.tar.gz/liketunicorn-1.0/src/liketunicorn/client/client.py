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


class SessionStateManager:
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


class SessionManager(SessionStateManager):
    def __init__(
        self,
        *,
        api: TelegramAPI,
        session: Optional[ClientSession] = None,
    ) -> None:
        super(SessionManager, self).__init__(session=session)

        self.api = api

    def build_data(self, request: Request) -> FormData:
        form = FormData(quote_fields=False)
        for key, value in request.data.items():
            if value is not None:
                form.add_field(key, prepare_value(value))
        if request.files:
            for key, value in request.files.items():
                form.add_field(key, value, filename=value.filename or key)
        return form

    def check_response(
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
                    "Exception %s: %s. Retry after %s."
                    % (method, description, parameters.retry_after)
                )
            if parameters.migrate_to_chat_id:
                raise TelegramMigrateToChat(
                    "Exception %s: %s. Migrate to chat id %s."
                    % (method, description, parameters.migrate_to_chat_id)
                )
        if status_code == HTTPStatus.BAD_REQUEST:
            raise TelegramBadRequest(
                "Exception %s: %s." % (method, description),
            )
        if status_code == HTTPStatus.NOT_FOUND:
            raise TelegramNotFound(
                "Exception %s: %s." % (method, description),
            )
        if status_code == HTTPStatus.CONFLICT:
            raise TelegramConflictError(
                "Exception %s: %s." % (method, description),
            )
        if status_code == HTTPStatus.UNAUTHORIZED:
            raise TelegramUnauthorizedError(
                "Exception %s: %s." % (method, description),
            )
        if status_code == HTTPStatus.FORBIDDEN:
            raise TelegramForbiddenError(
                "Exception %s: %s." % (method, description),
            )
        if status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE:
            raise TelegramEntityTooLarge(
                "Exception %s: %s." % (method, description),
            )
        if status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
            if "restart" in description:
                raise RestartingTelegram(
                    "Exception %s: %s." % (method, description),
                )
            raise TelegramServerError(
                "Exception %s: %s." % (method, description),
            )

        raise TelegramAPIError(
            "Exception %s: %s." % (method, description),
        )

    async def request(
        self, method: TelegramMethod[TelegramType], timeout: int = _REQUEST_TIMEOUT
    ) -> TelegramType:
        await self.create()

        request = method.request()
        url = self.api.api_url.format(method=request.method)
        data = self.build_data(request)

        try:
            async with self._session.post(url, data=data, timeout=timeout) as response:
                content = await response.text()
        except asyncio.TimeoutError:
            raise TelegramNetworkError("Exception %s: %s." % (method, "request timeout error"))
        except ClientError as e:
            raise TelegramNetworkError(
                "Exception for method %s: %s." % (method, f"{type(e).__name__}: {e}")
            )
        response = self.check_response(method=method, status_code=response.status, content=content)
        return cast(TelegramType, response.result)
