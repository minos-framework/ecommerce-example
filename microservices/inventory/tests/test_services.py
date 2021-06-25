"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
import sys
import unittest
from asyncio import gather
from pathlib import Path
from typing import NoReturn
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
from src import (
    Inventory,
    InventoryService,
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


class TestInventoryService(unittest.IsolatedAsyncioTestCase):
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

        self.service = InventoryService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_create_inventory(self):
        inventory = await self.service.create_inventory(1, 34)
        self.assertIsInstance(inventory, Inventory)
        self.assertEqual(1, inventory.product)
        self.assertEqual(34, inventory.amount)

    async def test_get_inventories(self):
        expected = await gather(
            self.service.create_inventory(1, 34),
            self.service.create_inventory(2, 12),
            self.service.create_inventory(3, 43),
        )
        ids = [v.id for v in expected]

        observed = await self.service.get_inventories(ids)
        self.assertEqual(expected, observed)


if __name__ == "__main__":
    unittest.main()
