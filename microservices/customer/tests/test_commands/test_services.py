from __future__ import annotations

import sys
import unittest
from uuid import uuid4

from minos.aggregate import DeletedAggregateException
from minos.networks import (
    Response,
    ResponseException,
)

from src import (
    Address,
    Customer,
    CustomerCommandService,
)
from tests.utils import (
    _FakeRequest,
    build_dependency_injector,
)


class TestCustomerCommandService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.injector = build_dependency_injector()
        await self.injector.wire(modules=[sys.modules[__name__]])

        self.service = CustomerCommandService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_create_customer(self):
        request = _FakeRequest(
            {"name": "John", "surname": "Coltrane", "address": {"street": "Green Dolphin Street", "street_no": 42}}
        )
        response = await self.service.create_customer(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()
        expected = Customer(
            "John",
            "Coltrane",
            Address(street="Green Dolphin Street", street_no=42),
            created_at=observed.created_at,
            updated_at=observed.updated_at,
            uuid=observed.uuid,
            version=observed.version,
        )

        self.assertEqual(expected, observed)

    async def test_delete_customer(self):
        customer = await Customer.create("John", "Coltrane", Address(street="Green Dolphin Street", street_no=42),)

        request = _FakeRequest({"uuid": customer.uuid})
        await self.service.delete_customer(request)

        with self.assertRaises(DeletedAggregateException):
            await Customer.get(customer.uuid)

    async def test_delete_customer_bad_request(self):
        customer = await Customer.create("John", "Coltrane", Address(street="Green Dolphin Street", street_no=42),)

        request = _FakeRequest({"uusdfasfid": customer.uuid})
        with self.assertRaises(ResponseException):
            await self.service.delete_customer(request)

    async def test_delete_customer_not_exist(self):
        request = _FakeRequest({"uuid": uuid4()})
        with self.assertRaises(ResponseException):
            await self.service.delete_customer(request)


if __name__ == "__main__":
    unittest.main()
