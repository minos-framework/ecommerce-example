from __future__ import (
    annotations,
)

import base64
import json
import sys
import unittest
from pathlib import (
    Path,
)
from typing import (
    NoReturn,
)
from uuid import (
    UUID,
    uuid4,
)

import jwt
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
)
from src import (
    LoginQueryService,
    UserQueryRepository,
)
from src.queries import (
    AlreadyExists,
)


class _FakeRawRequest:
    def __init__(self, headers: dict[str, str]):
        self.headers = headers


class _FakeRestRequest(RestRequest):
    def __init__(self, username: str, password: str):
        encoded_credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
        headers = {"Authorization": f"Basic {encoded_credentials}"}
        self.raw_request = _FakeRawRequest(headers)


class _FakeBroker(MinosBroker):
    async def send(self, items: list[Model], **kwargs) -> NoReturn:
        pass


class _FakeSagaManager(MinosSagaManager):
    async def _run_new(self, name: str, **kwargs) -> UUID:
        pass

    async def _load_and_run(self, reply: CommandReply, **kwargs) -> UUID:
        pass


class TestLoginQueryService(unittest.IsolatedAsyncioTestCase):
    CONFIG_FILE_PATH = Path(__file__).parents[2] / "config.yml"

    async def asyncSetUp(self) -> None:
        self.config = MinosConfig(self.CONFIG_FILE_PATH)
        self.injector = DependencyInjector(
            self.config,
            saga_manager=_FakeSagaManager,
            event_broker=_FakeBroker,
            repository=InMemoryRepository,
            snapshot=InMemorySnapshot,
            user_repository=UserQueryRepository,
        )
        await self.injector.wire(modules=[sys.modules[__name__]])

        self.service = LoginQueryService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_get_token(self):
        uuid = uuid4()
        username = "test_username"  # UUID just to ensure its unique
        password = "test_password"

        try:
            await self.service.repository.create_user(uuid, username, password, True)
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
