from __future__ import annotations

import sys
import unittest
from asyncio import gather
from unittest.mock import AsyncMock
from uuid import uuid4

from minos.networks import (
    Response,
    ResponseException,
)
from minos.saga import SagaContext

from src import (
    Credentials,
    CredentialsCommandService,
)
from tests.utils import (
    _FakeRequest,
    _FakeSagaExecution,
    build_dependency_injector,
)


class TestCredentialsCommandService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.injector = build_dependency_injector()
        await self.injector.wire(modules=[sys.modules[__name__]])
        self.service = CredentialsCommandService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_create_credentials(self):
        expected = await Credentials.create("foo", "bar", active=True, user=uuid4())

        self.injector.injections["saga_manager"].run = AsyncMock(
            return_value=_FakeSagaExecution(SagaContext(credentials=expected))
        )

        request = _FakeRequest(
            {"username": "foo", "password": "bar", "name": "John", "surname": "Snow", "address": "Winterfell"}
        )
        response = await self.service.create_credentials(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()
        self.assertEqual({"user": expected.user}, observed)

    async def test_create_credentials_raises_duplicated_username(self):
        await Credentials.create("foo", "bar", True, uuid4())

        request = _FakeRequest({"username": "foo", "password": "bar"})

        with self.assertRaises(ResponseException):
            await self.service.create_credentials(request)

    @unittest.skip
    async def test_create_credentials_concurrently(self):
        request = _FakeRequest(
            {"username": "foo", "password": "bar", "name": "John", "surname": "Snow", "address": "Winterfell"}
        )

        observed = await gather(*(self.service.create_credentials(request) for _ in range(10)), return_exceptions=True)

        self.assertEqual(1, sum(not isinstance(o, ResponseException) for o in observed))


if __name__ == "__main__":
    unittest.main()
