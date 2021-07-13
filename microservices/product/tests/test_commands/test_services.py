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
    Inventory,
    Product,
    ProductCommandService,
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


class TestProductCommandService(unittest.IsolatedAsyncioTestCase):
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

        self.service = ProductCommandService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_create_product(self):
        product = await self.service.create_product("Cacao", "1KG", 3)
        self.assertIsInstance(product, Product)
        self.assertIsInstance(product.code, str)
        self.assertEqual(6, len(product.code))
        self.assertEqual("Cacao", product.title)
        self.assertEqual(3, product.price)

    async def test_get_products(self):
        expected = await gather(
            Product.create("abc", "Cacao", "1KG", 3, Inventory(0)),
            Product.create("def", "Cafe", "2KG", 1, Inventory(0)),
            Product.create("ghi", "Milk", "1L", 2, Inventory(0)),
        )
        uuids = [v.uuid for v in expected]

        observed = await self.service.get_products(uuids)
        self.assertEqual(expected, observed)

    async def test_update_inventory(self):
        product = await Product.create("abc", "Cacao", "1KG", 3, Inventory(12))
        await self.service.update_inventory(product.uuid, 56)
        await product.refresh()
        self.assertEqual(Inventory(56), product.inventory)

    async def test_update_inventory_diff(self):
        product = await Product.create("abc", "Cacao", "1KG", 3, Inventory(12))
        await self.service.update_inventory_diff(product.uuid, 12)
        await product.refresh()
        self.assertEqual(Inventory(24), product.inventory)

        await self.service.update_inventory_diff(product.uuid, -10)
        await product.refresh()
        self.assertEqual(Inventory(14), product.inventory)


if __name__ == "__main__":
    unittest.main()
