"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from __future__ import (
    annotations,
)

import sys
import unittest.async_case
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
)
from unittest.mock import (
    call,
    patch,
)
from uuid import (
    UUID,
    uuid4,
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
    Order,
    OrderController,
)


class _FakeRequest(Request):
    """For testing purposes"""

    def __init__(self, content):
        super().__init__()
        self._content = content

    async def content(self):
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


class TestProductController(unittest.IsolatedAsyncioTestCase):
    CONFIG_FILE_PATH = Path(__file__).parents[1] / "config.yml"

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

        self.controller = OrderController()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_create_order(self):
        uuid = uuid4()

        async def _fn(*args, **kwargs):
            return uuid

        with patch("src.OrderService.create_order") as mock:
            mock.side_effect = _fn

            request = _FakeRequest({"products": [1, 2, 3]})
            response = await self.controller.create_order(request)

            self.assertIsInstance(response, Response)

            observed = await response.content()
            self.assertEqual([str(uuid)], observed)
            self.assertEqual(call(products=[1, 2, 3]), mock.call_args)

    async def test_get_orders(self):
        now = datetime.now(tz=timezone.utc)

        expected = await gather(
            Order.create([1, 2, 3], 1, "created", now, now), Order.create([1, 1, 1], 2, "cancelled", now, now),
        )

        request = _FakeRequest({"ids": [v.id for v in expected]})

        response = await self.controller.get_orders(request)
        observed = await response.content()
        self.assertEqual(expected, observed)


if __name__ == "__main__":
    unittest.main()
