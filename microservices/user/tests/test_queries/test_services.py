"""tests.queries.services module."""

from __future__ import (
    annotations,
)

import sys
import unittest
from asyncio import (
    gather,
)
from datetime import (
    datetime,
    timezone,
)
from pathlib import (
    Path,
)
from typing import (
    NoReturn,
    Optional,
)
from uuid import (
    UUID,
    uuid4,
)

from cached_property import (
    cached_property,
)
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
    Request,
)
from src import (
    User,
    UserQueryService,
)


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
    """For testing purposes."""

    async def send(self, items: list[Model], **kwargs) -> NoReturn:
        """For testing purposes."""


class _FakeSagaManager(MinosSagaManager):
    """For testing purposes."""

    async def _run_new(self, name: str, **kwargs) -> UUID:
        """For testing purposes."""

    async def _load_and_run(self, reply: CommandReply, **kwargs) -> UUID:
        """For testing purposes."""


class TestUserQueryService(unittest.IsolatedAsyncioTestCase):
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

        self.service = UserQueryService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_get_users(self):
        now = datetime.now(tz=timezone.utc)

        expected = await gather(
            User.create("foo", "bar", "active", {"street": "hello", "street_no": 1}, now),
            User.create("one", "two", "inactive", {"street": "hola", "street_no": 0}, now),
        )

        request = _FakeRequest({"uuids": [v.uuid for v in expected]})

        response = await self.service.get_users(request)
        observed = await response.content()

        self.assertEqual(expected, observed)

    async def test_get_user(self):
        now = datetime.now(tz=timezone.utc)

        expected = await User.create("foo", "bar", "active", {"street": "hello", "street_no": 1}, now)

        request = _FakeRequest({"uuid": expected.uuid})

        response = await self.service.get_user(request)
        observed = await response.content()

        self.assertEqual(expected, observed)


if __name__ == "__main__":
    unittest.main()
