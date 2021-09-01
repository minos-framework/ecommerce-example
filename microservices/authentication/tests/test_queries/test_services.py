from __future__ import annotations

import base64
import json
import sys
import unittest
from pathlib import Path
from typing import (
    NoReturn,
    Any,
    Optional,
)
from uuid import (
    UUID,
    uuid4,
)

import jwt
from cached_property import cached_property
from minos.common import (
    CommandReply,
    DependencyInjector,
    InMemoryRepository,
    InMemorySnapshot,
    MinosBroker,
    MinosConfig,
    MinosSagaManager,
    Model,
)
from minos.networks import (
    RestRequest,
    Request,
    ResponseException,
)
from src import (
    CredentialsQueryRepository,
    CredentialsQueryService,
)
from src.queries import AlreadyExists
from src.queries.exceptions import DoesNotExist


class _FakeRawRequest:
    def __init__(self, headers: dict[str, str]):
        self.headers = headers


class _FakeRestRequest(RestRequest):
    def __init__(self, username: str, password: str):
        encoded_credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
        headers = {"Authorization": f"Basic {encoded_credentials}"}
        self.raw_request = _FakeRawRequest(headers)


class _FakeRequest(Request):
    """For testing purposes"""

    def __init__(self, content):
        super().__init__()
        self._content = content

    @cached_property
    def user(self) -> Optional[UUID]:
        """For testing purposes"""
        return uuid4()

    async def content(self, **kwargs):
        """For testing purposes"""
        return self._content

    def __eq__(self, other: _FakeRequest) -> bool:
        return self._content == other._content and self.user == other.user

    def __repr__(self) -> str:
        return str()


class _FakeBroker(MinosBroker):
    async def send(self, items: list[Model], **kwargs) -> NoReturn:
        pass


class _FakeSagaManager(MinosSagaManager):
    async def _run_new(self, name: str, **kwargs) -> UUID:
        pass

    async def _load_and_run(self, reply: CommandReply, **kwargs) -> UUID:
        pass


class TestCredentialsQueryService(unittest.IsolatedAsyncioTestCase):
    CONFIG_FILE_PATH = Path(__file__).parents[2] / "config.yml"

    async def asyncSetUp(self) -> None:
        self.config = MinosConfig(self.CONFIG_FILE_PATH)
        self.injector = DependencyInjector(
            self.config,
            saga_manager=_FakeSagaManager,
            event_broker=_FakeBroker,
            repository=InMemoryRepository,
            snapshot=InMemorySnapshot,
            credentials_repository=CredentialsQueryRepository,
        )
        await self.injector.wire(modules=[sys.modules[__name__]])

        self.service = CredentialsQueryService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_get_token(self):
        uuid = uuid4()
        username = "test_username"  # UUID just to ensure its unique
        password = "test_password"

        try:
            await self.service.repository.create_credentials(uuid, username, password, True)
        except AlreadyExists:
            row = await self.service.repository.get_by_username(username)
            uuid = UUID(str(row["uuid"]))
            username = row["username"]
            password = row["password"]

        fake_request = _FakeRestRequest(username, password)
        response = await self.service.get_token(fake_request)
        token = await response.content()
        payload = jwt.decode(token, options={"verify_signature": False})
        observed_uuid = UUID(payload["sub"])

        self.assertEqual(uuid, observed_uuid)

    async def test_get_by_username_does_not_exist(self):
        wrong_username = "should_not_exist"

        with self.assertRaises(ResponseException):
            fake_request = _FakeRequest({"username": wrong_username})
            response = await self.service.get_by_username(fake_request)


if __name__ == "__main__":
    unittest.main()
