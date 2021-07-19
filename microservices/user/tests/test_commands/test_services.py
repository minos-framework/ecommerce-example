"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
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
)
from pathlib import (
    Path,
)
from typing import (
    NoReturn,
)
from uuid import (
    UUID,
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
    Request,
    Response,
)
from src import (
    Address,
    User,
    UserCommandService,
)


class _FakeRequest(Request):
    """For testing purposes"""

    def __init__(self, content):
        super().__init__()
        self._content = content

    async def content(self, **kwargs):
        """For testing purposes"""
        return self._content

    def __eq__(self, other: _FakeRequest) -> bool:
        return self._content == other._content

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


class TestUserCommandService(unittest.IsolatedAsyncioTestCase):
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

        self.service = UserCommandService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_create_user(self):
        request = _FakeRequest({"username": "john_coltrane", "status": "created",
                                "address": {"street": "Green Dolphin Street", "street_no": 42}})
        response = await self.service.create_user(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()
        expected = User(
            "john_coltrane", "created", Address(street="Green Dolphin Street", street_no=42),
            created_at=observed.created_at, uuid=observed.uuid, version=observed.version
        )

        self.assertEqual(expected, observed)


if __name__ == "__main__":
    unittest.main()
