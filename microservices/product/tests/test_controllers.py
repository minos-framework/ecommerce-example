"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
import sys
import unittest.async_case
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
    Request,
    Response,
)
from src import (
    Inventory,
    Product,
    ProductController,
)


class _FakeRequest(Request):
    """For testing purposes"""

    def __init__(self, content):
        super().__init__()
        self._content = content

    async def content(self):
        """For testing purposes"""
        return self._content


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

        self.controller = ProductController()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_create_product(self):
        request = _FakeRequest([{"code": "abc", "title": "Cacao", "description": "1KG", "price": 3}])
        response = await self.controller.create_product(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()
        expected = [Product("abc", "Cacao", "1KG", 3, Inventory(0), id=observed[0].id, version=observed[0].version)]
        self.assertEqual(expected, observed)

    async def test_get_products(self):
        expected = await gather(
            Product.create("abc", "Cacao", "1KG", 3, Inventory(0)),
            Product.create("def", "Cafe", "2KG", 1, Inventory(0)),
            Product.create("ghi", "Milk", "1L", 2, Inventory(0)),
        )
        ids = [v.id for v in expected]
        request = _FakeRequest(ids)

        response = await self.controller.get_products(request)
        observed = await response.content()
        self.assertEqual(expected, observed)

    async def test_update_inventory(self):
        product = await Product.create("abc", "Cacao", "1KG", 3, Inventory(12))
        expected = [Product("abc", "Cacao", "1KG", 3, Inventory(56), id=product.id, version=2)]

        request = _FakeRequest([{"product_id": product.id, "amount": 56}])
        response = await self.controller.update_inventory(request)
        observed = await response.content()
        self.assertEqual(expected, observed)

    async def test_update_inventory_diff(self):
        product = await Product.create("abc", "Cacao", "1KG", 3, Inventory(12))
        expected = [Product("abc", "Cacao", "1KG", 3, Inventory(24), id=product.id, version=2)]

        request = _FakeRequest([{"product_id": product.id, "amount_diff": 12}])
        response = await self.controller.update_inventory_diff(request)
        observed = await response.content()
        self.assertEqual(expected, observed)

    async def test_validate_products_true(self):
        expected = await gather(
            Product.create("abc", "Cacao", "1KG", 3, Inventory(0)),
            Product.create("def", "Cafe", "2KG", 1, Inventory(0)),
            Product.create("ghi", "Milk", "1L", 2, Inventory(0)),
        )
        ids = [v.id for v in expected]
        request = _FakeRequest(ids)
        response = await self.controller.validate_products(request)
        observed = await response.content()
        self.assertTrue(observed[0].exist)

    async def test_validate_products_false(self):
        request = _FakeRequest([9999])
        response = await self.controller.validate_products(request)
        observed = await response.content()
        self.assertFalse(observed[0].exist)


if __name__ == "__main__":
    unittest.main()
