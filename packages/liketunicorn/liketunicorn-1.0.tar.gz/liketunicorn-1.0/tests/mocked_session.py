from __future__ import annotations

from collections import deque
from typing import Deque, Optional, Type

from aiohttp import ClientSession

from liketunicorn.api import TelegramAPI
from liketunicorn.client.client import SessionManager, SessionStateManager
from liketunicorn.client.methods import Request, Response, TelegramMethod, TelegramType
from liketunicorn.client.types import ResponseParameters


class Session:
    class ResponseGenerator:
        def __init__(self, session: Session) -> None:
            self._accessor = session

        def add_result_for(
            self,
            method: Type[TelegramMethod[TelegramType]],
            ok: bool,
            result: Optional[TelegramType] = None,
            description: Optional[str] = None,
            error_code: int = 200,
            migrate_to_chat_id: Optional[int] = None,
            retry_after: Optional[int] = None,
        ) -> Response[TelegramType]:
            response = Response[method.__returns__](
                ok=ok,
                result=result,
                description=description,
                error_code=error_code,
                parameters=ResponseParameters(
                    migrate_to_chat_id=migrate_to_chat_id,
                    retry_after=retry_after,
                ),
            )
            self._accessor.add_response(response)
            return response

    def __init__(self) -> None:
        self.requests: Deque[Request] = deque()
        self.responses: Deque[Response[TelegramType]] = deque()
        self.response_generator = Session.ResponseGenerator(self)

    def get_request(self) -> Request:
        return self.requests.pop()

    def get_response(self) -> Response[TelegramType]:
        return self.responses.pop()

    def add_request(self, request: Request) -> Request:
        self.requests.append(request)
        return request

    def add_response(self, response: Response[TelegramType]) -> Response[TelegramType]:
        self.responses.append(response)
        return response

    def add_result_for(
        self,
        method: Type[TelegramMethod[TelegramType]],
        ok: bool,
        result: Optional[TelegramType] = None,
        description: Optional[str] = None,
        error_code: int = 200,
        migrate_to_chat_id: Optional[int] = None,
        retry_after: Optional[int] = None,
    ) -> Response[TelegramType]:
        return self.response_generator.add_result_for(
            method=method,
            ok=ok,
            result=result,
            description=description,
            error_code=error_code,
            migrate_to_chat_id=migrate_to_chat_id,
            retry_after=retry_after,
        )


class MockedSessionStateManager(SessionStateManager):
    """
    First of all we need to override the class.
    """

    def __init__(self, *, session: Optional[ClientSession] = None) -> None:
        session = None
        super(MockedSessionStateManager, self).__init__(session=session)

    async def create(self) -> None:
        # We need to remove the ability to create a `aiohttp.ClientSession`
        ...

    async def close(self) -> None:
        # And we need to remove the ability to close a `aiohttp.ClientSession`
        ...


class MockedSessionManager(SessionManager, MockedSessionStateManager):
    """
    Overrides the `request` method.
    """

    def __init__(
        self,
        *,
        api: TelegramAPI,
        session: Optional[ClientSession] = None,
    ) -> None:
        session = None
        super(MockedSessionManager, self).__init__(api=api, session=session)
        self.session = Session()

    @property
    def mock(self) -> Session:
        return self.session

    async def request(
        self, method: TelegramMethod[TelegramType], timeout: int = 60.0
    ) -> TelegramType:
        await self.create()

        request = method.request()
        self.session.add_request(request)
        response = self.session.get_response()
        self.check_response(
            method=method, status_code=response.error_code, content=response.json()
        )
        return response.result
