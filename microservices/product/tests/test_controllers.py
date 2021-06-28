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
    Product,
    ProductController,
    ProductService,
    Inventory,
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
        service = ProductService()
        expected = await gather(
            service.create_product("abc", "Cacao", "1KG", 3),
            service.create_product("def", "Cafe", "2KG", 1),
            service.create_product("ghi", "Milk", "1L", 2),
        )
        ids = [v.id for v in expected]
        request = _FakeRequest(ids)

        response = await self.controller.get_products(request)
        observed = await response.content()
        self.assertEqual(expected, observed)


if __name__ == "__main__":
    unittest.main()
