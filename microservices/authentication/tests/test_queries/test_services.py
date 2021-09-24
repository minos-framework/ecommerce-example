from __future__ import annotations

import base64
import sys
import unittest
from asyncio import gather
from pathlib import Path
from uuid import (
    UUID,
    uuid4,
)

import jwt
from minos.common import (
    DependencyInjector,
    InMemoryRepository,
    InMemorySnapshot,
    MinosConfig,
)
from minos.networks import RestRequest

from src import (
    CredentialsQueryRepository,
    CredentialsQueryService,
)
from src.queries import AlreadyExists
from tests.utils import (
    _FakeBroker,
    _FakeSagaManager,
)


class _FakeRawRequest:
    def __init__(self, headers: dict[str, str]):
        self.headers = headers


class _FakeRestRequest(RestRequest):
    def __init__(self, username: str, password: str):
        encoded_credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
        headers = {"Authorization": f"Basic {encoded_credentials}"}
        self.raw_request = _FakeRawRequest(headers)


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
            credentials_repository=CredentialsQueryRepository.from_config(
                self.config, database=self.config.repository.database
            ),
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


if __name__ == "__main__":
    unittest.main()
