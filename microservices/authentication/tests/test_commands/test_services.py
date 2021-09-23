from __future__ import (
    annotations,
)

import sys
import unittest
from asyncio import (
    gather,
)

from minos.networks import (
    Response,
    ResponseException,
)

from src import (
    Credentials,
    CredentialsCommandService,
)
from tests.utils import (
    _FakeRequest,
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
        request = _FakeRequest({"username": "test_name", "password": "test_password"})
        response = await self.service.create_credentials(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()
        expected = Credentials(
            "test_name",
            "test_password",
            True,
            uuid=observed.uuid,
            version=observed.version,
            created_at=observed.created_at,
            updated_at=observed.updated_at,
        )
        self.assertEqual(expected, observed)

    async def test_create_credentials_raises_duplicated_username(self):
        await Credentials.create("foo", "bar", True)

        request = _FakeRequest({"username": "foo", "password": "bar"})

        with self.assertRaises(ResponseException):
            await self.service.create_credentials(request)

    async def test_create_credentials_concurrently(self):
        request = _FakeRequest({"username": "foo", "password": "bar"})

        observed = await gather(*(self.service.create_credentials(request) for _ in range(10)), return_exceptions=True)

        self.assertEqual(1, sum(not isinstance(o, ResponseException) for o in observed))


if __name__ == "__main__":
    unittest.main()
