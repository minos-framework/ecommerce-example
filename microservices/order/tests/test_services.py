"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
import sys
import unittest
from asyncio import (
    gather,
)
from datetime import datetime, timezone, timedelta
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
)
from src import (
    Order,
    OrderService,
)


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


class TestProductService(unittest.IsolatedAsyncioTestCase):
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

        self.service = OrderService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_create_order(self):
        order = await self.service.create_order([1, 2, 3])
        self.assertIsInstance(order, Order)
        self.assertEqual([1, 2, 3], order.products)
        self.assertEqual("created", order.status)
        self.assertIsInstance(order.created_at, datetime)
        self.assertIsInstance(order.updated_at, datetime)

    async def test_get_orders(self):
        now = datetime.now(tz=timezone.utc)
        now -= timedelta(microseconds=now.microsecond)

        expected = await gather(
            Order.create([1, 2, 3], "created", now, now),
            Order.create([1, 1, 1], "cancelled", now, now),
        )
        ids = [v.id for v in expected]

        observed = await self.service.get_orders(ids)
        self.assertEqual(expected, observed)


if __name__ == "__main__":
    unittest.main()
