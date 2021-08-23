from __future__ import annotations

import base64
import json
import sys
import unittest
from pathlib import Path
from typing import NoReturn
from uuid import UUID
from minos.networks import RestRequest
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
from src import (
    LoginQueryService,
    UserQueryRepository,
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
        username = "test_username"
        password = "test_password"

        await self.service.repository.create_user(username, password, True)

        fake_request = _FakeRestRequest(username, password)
        response = await self.service.get_token(fake_request)
        token = await response.content()
        token = token.split(".")
        observed_username = json.loads(base64.b64decode(token[1]).decode())["name"]

        self.assertEqual(username, observed_username)


if __name__ == "__main__":
    unittest.main()
