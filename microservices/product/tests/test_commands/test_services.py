from __future__ import (
    annotations,
)

import sys
import unittest
from collections import (
    defaultdict,
)

from minos.networks import (
    Response,
)

from src import (
    Inventory,
    Product,
    ProductCommandService,
)
from tests.utils import (
    _FakeRequest,
    build_dependency_injector,
)


class TestProductCommandService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.injector = build_dependency_injector()
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
            observed.code,
            "Cacao",
            "1KG",
            3,
            Inventory(amount=0, reserved=0, sold=0),
            uuid=observed.uuid,
            version=observed.version,
            created_at=observed.created_at,
            updated_at=observed.updated_at,
        )

        self.assertEqual(expected, observed)

    async def test_update_product(self):
        product = await Product.create("abc", "Cacao", "1KG", 3, Inventory(amount=12, reserved=0, sold=0))

        request = _FakeRequest({"title": "Cola-Cao", "description": "1.5KG", "price": 4}, {"uuid": product.uuid})
        response = await self.service.update_product(request)
        observed = await response.content()
        expected = Product(
            "abc",
            "Cola-Cao",
            "1.5KG",
            4,
            Inventory(amount=12, reserved=0, sold=0),
            uuid=product.uuid,
            version=2,
            created_at=observed.created_at,
            updated_at=observed.updated_at,
        )
        self.assertEqual(expected, observed)

    async def test_update_product_diff(self):
        product = await Product.create("abc", "Cacao", "1KG", 3, Inventory(amount=12, reserved=0, sold=0))

        request = _FakeRequest({"title": "Cola-Cao"}, {"uuid": product.uuid})
        response = await self.service.update_product_diff(request)
        observed = await response.content()
        expected = Product(
            "abc",
            "Cola-Cao",
            "1KG",
            3,
            Inventory(amount=12, reserved=0, sold=0),
            uuid=product.uuid,
            created_at=observed.created_at,
            updated_at=observed.updated_at,
            version=2,
        )
        self.assertEqual(expected, observed)

    async def test_update_inventory(self):
        product = await Product.create("abc", "Cacao", "1KG", 3, Inventory(amount=12, reserved=0, sold=0))

        request = _FakeRequest({"amount": 56}, {"uuid": product.uuid})
        response = await self.service.update_inventory(request)
        observed = await response.content()
        expected = Product(
            "abc",
            "Cacao",
            "1KG",
            3,
            Inventory(amount=56, reserved=0, sold=0),
            uuid=product.uuid,
            created_at=observed.created_at,
            updated_at=observed.updated_at,
            version=2,
        )
        self.assertEqual(expected, observed)

    async def test_update_inventory_diff(self):
        product = await Product.create("abc", "Cacao", "1KG", 3, Inventory(amount=12, reserved=0, sold=0))

        request = _FakeRequest({"amount_diff": 12}, {"uuid": product.uuid})
        response = await self.service.update_inventory_diff(request)
        observed = await response.content()
        expected = Product(
            "abc",
            "Cacao",
            "1KG",
            3,
            Inventory(amount=24, reserved=0, sold=0),
            uuid=product.uuid,
            created_at=observed.created_at,
            updated_at=observed.updated_at,
            version=2,
        )
        self.assertEqual(expected, observed)

    async def test_reserve_product(self):
        product = await Product.create("abc", "Cacao", "1KG", 3, Inventory(amount=12, reserved=0, sold=0))

        quantities = defaultdict(int)
        quantities[str(product.uuid)] += 3

        request = _FakeRequest({"quantities": quantities})
        await self.service.reserve_products(request)
        obtained = await Product.get(product.uuid)
        expected = Product(
            "abc",
            "Cacao",
            "1KG",
            3,
            Inventory(amount=12, reserved=3, sold=0),
            uuid=product.uuid,
            created_at=obtained.created_at,
            updated_at=obtained.updated_at,
            version=2,
        )

        self.assertEqual(expected, obtained)

    async def test_purchase_product(self):
        product = await Product.create("abc", "Cacao", "1KG", 3, Inventory(amount=12, reserved=0, sold=0))

        quantities = defaultdict(int)
        quantities[str(product.uuid)] += 3

        request = _FakeRequest({"quantities": quantities})
        await self.service.reserve_products(request)

        obtained = await Product.get(product.uuid)

        expected = Product(
            "abc",
            "Cacao",
            "1KG",
            3,
            Inventory(amount=12, reserved=3, sold=0),
            uuid=product.uuid,
            created_at=obtained.created_at,
            updated_at=obtained.updated_at,
            version=2,
        )

        self.assertEqual(expected, obtained)

        await self.service.purchase_products(request)

        obtained = await Product.get(product.uuid)
        expected = Product(
            "abc",
            "Cacao",
            "1KG",
            3,
            Inventory(amount=9, reserved=0, sold=3),
            uuid=product.uuid,
            created_at=obtained.created_at,
            updated_at=obtained.updated_at,
            version=3,
        )

        self.assertEqual(expected, obtained)


if __name__ == "__main__":
    unittest.main()
