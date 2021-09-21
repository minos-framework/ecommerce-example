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
from collections import (
    defaultdict,
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
    Response,
)
from src import (
    Inventory,
    Product,
    ProductCommandService,
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
        request = _FakeRequest({"title": "Cacao", "description": "1KG", "price": 3})
        response = await self.service.create_product(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()
        expected = Product(
            "Cacao",
            "1KG",
            3,
            code=observed.code,
            inventory=Inventory(amount=0, reserved=0, sold=0),
            uuid=observed.uuid,
            version=observed.version,
            created_at=observed.created_at,
            updated_at=observed.updated_at,
        )

        self.assertEqual(expected, observed)

    async def test_update_product(self):
        product = await Product.create(
            "Cacao", "1KG", 3, code="abc", inventory=Inventory(amount=12, reserved=0, sold=0)
        )

        request = _FakeRequest({"uuid": product.uuid, "title": "Cola-Cao", "description": "1.5KG", "price": 4})
        response = await self.service.update_product(request)
        observed = await response.content()
        expected = Product(
            "Cola-Cao",
            "1.5KG",
            4,
            code="abc",
            inventory=Inventory(amount=12, reserved=0, sold=0),
            uuid=product.uuid,
            version=2,
            created_at=observed.created_at,
            updated_at=observed.updated_at,
        )
        self.assertEqual(expected, observed)

    async def test_update_product_diff(self):
        product = await Product.create(
            "Cacao", "1KG", 3, code="abc", inventory=Inventory(amount=12, reserved=0, sold=0)
        )

        request = _FakeRequest({"uuid": product.uuid, "title": "Cola-Cao"})
        response = await self.service.update_product_diff(request)
        observed = await response.content()
        expected = Product(
            "Cola-Cao",
            "1KG",
            3,
            code="abc",
            inventory=Inventory(amount=12, reserved=0, sold=0),
            uuid=product.uuid,
            created_at=observed.created_at,
            updated_at=observed.updated_at,
            version=2,
        )
        self.assertEqual(expected, observed)

    async def test_update_inventory(self):
        product = await Product.create(
            "Cacao", "1KG", 3, code="abc", inventory=Inventory(amount=12, reserved=0, sold=0)
        )

        request = _FakeRequest({"uuid": product.uuid, "amount": 56})
        response = await self.service.update_inventory(request)
        observed = await response.content()
        expected = Product(
            "Cacao",
            "1KG",
            3,
            code="abc",
            inventory=Inventory(amount=56, reserved=0, sold=0),
            uuid=product.uuid,
            created_at=observed.created_at,
            updated_at=observed.updated_at,
            version=2,
        )
        self.assertEqual(expected, observed)

    async def test_update_inventory_diff(self):
        product = await Product.create(
            "Cacao", "1KG", 3, code="abc", inventory=Inventory(amount=12, reserved=0, sold=0)
        )

        request = _FakeRequest({"uuid": product.uuid, "amount_diff": 12})
        response = await self.service.update_inventory_diff(request)
        observed = await response.content()
        expected = Product(
            "Cacao",
            "1KG",
            3,
            code="abc",
            inventory=Inventory(amount=24, reserved=0, sold=0),
            uuid=product.uuid,
            created_at=observed.created_at,
            updated_at=observed.updated_at,
            version=2,
        )
        self.assertEqual(expected, observed)

    async def test_reserve_product(self):
        product = await Product.create(
            "Cacao", "1KG", 3, code="abc", inventory=Inventory(amount=12, reserved=0, sold=0)
        )

        quantities = defaultdict(int)
        quantities[str(product.uuid)] += 3

        request = _FakeRequest({"quantities": quantities})
        await self.service.reserve_products(request)
        obtained = await Product.get(product.uuid)
        expected = Product(
            "Cacao",
            "1KG",
            3,
            code="abc",
            inventory=Inventory(amount=12, reserved=3, sold=0),
            uuid=product.uuid,
            created_at=obtained.created_at,
            updated_at=obtained.updated_at,
            version=2,
        )

        self.assertEqual(expected, obtained)

    async def test_purchase_product(self):
        product = await Product.create(
            "Cacao", "1KG", 3, code="abc", inventory=Inventory(amount=12, reserved=0, sold=0)
        )

        quantities = defaultdict(int)
        quantities[str(product.uuid)] += 3

        request = _FakeRequest({"quantities": quantities})
        await self.service.reserve_products(request)

        obtained = await Product.get(product.uuid)

        expected = Product(
            "Cacao",
            "1KG",
            3,
            code="abc",
            inventory=Inventory(amount=12, reserved=3, sold=0),
            uuid=product.uuid,
            created_at=obtained.created_at,
            updated_at=obtained.updated_at,
            version=2,
        )

        self.assertEqual(expected, obtained)

        await self.service.purchase_products(request)

        obtained = await Product.get(product.uuid)
        expected = Product(
            "Cacao",
            "1KG",
            3,
            code="abc",
            inventory=Inventory(amount=9, reserved=0, sold=3),
            uuid=product.uuid,
            created_at=obtained.created_at,
            updated_at=obtained.updated_at,
            version=3,
        )

        self.assertEqual(expected, obtained)


if __name__ == "__main__":
    unittest.main()
