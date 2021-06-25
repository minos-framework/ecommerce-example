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

from minos.common import (
    DependencyInjector,
    MinosConfig,
    PostgreSqlRepository,
    PostgreSqlSnapshot,
)
from minos.networks import (
    EventBroker,
)
from minos.saga import (
    SagaManager,
)
from src import (
    Product,
    ProductService,
)


class TestProductService(unittest.IsolatedAsyncioTestCase):
    CONFIG_FILE_PATH = Path(__file__).parents[1] / "config.yml"

    async def asyncSetUp(self) -> None:
        self.config = MinosConfig(self.CONFIG_FILE_PATH)
        self.injector = DependencyInjector(
            self.config,
            saga_manager=SagaManager,
            event_broker=EventBroker,
            repository=PostgreSqlRepository,
            snapshot=PostgreSqlSnapshot,
        )
        await self.injector.wire(modules=[sys.modules[__name__]])

        self.service = ProductService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_create_product(self):
        product = await self.service.create_product("abc", "Cacao", "1KG", 3)
        self.assertIsInstance(product, Product)
        self.assertEqual("abc", product.code)
        self.assertEqual("Cacao", product.title)
        self.assertEqual(3, product.price)

    async def test_get_products(self):
        expected = await gather(
            self.service.create_product("abc", "Cacao", "1KG", 3),
            self.service.create_product("def", "Cafe", "2KG", 1),
            self.service.create_product("ghi", "Milk", "1L", 2),
        )
        ids = [v.id for v in expected]

        observed = await self.service.get_products(ids)
        self.assertEqual(expected, observed)


if __name__ == "__main__":
    unittest.main()
