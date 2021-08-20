from __future__ import annotations

import sys
import unittest
from pathlib import Path
from typing import (
    NoReturn,
    Optional,
)
from uuid import UUID

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
from minos.networks import RestRequest
from src import (
    LoginQueryService,
    User,
)


class _FakeRequest(RestRequest):
    def __init__(self, content):
        super().__init__()
        self._content = content

    def user(self) -> Optional[UUID]:
        pass

    async def content(self, **kwargs):
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
        )
        await self.injector.wire(modules=[sys.modules[__name__]])

        self.service = LoginQueryService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_get_token(self):
        expected = await User.create("test_name", "test_password", True)
        request = _FakeRequest({"uuids": [v.uuid for v in expected]})

        response = await self.service.get_token(request)
        observed = await response.content()
        self.assertEqual(expected, observed)


if __name__ == "__main__":
    unittest.main()
