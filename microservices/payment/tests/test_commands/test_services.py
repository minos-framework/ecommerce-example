from __future__ import (
    annotations,
)

import sys
import unittest

from minos.networks import (
    InMemoryRequest,
    Response,
)

from src import (
    Payment,
    PaymentCommandService,
)
from tests.utils import (
    build_dependency_injector,
)


class TestPaymentCommandService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.injector = build_dependency_injector()
        await self.injector.wire(modules=[sys.modules[__name__]])

        self.service = PaymentCommandService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_create_payment(self):
        request = InMemoryRequest({"credit_number": 1234, "amount": 3.4})
        response = await self.service.create_payment(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()
        expected = Payment(
            1234,
            3.4,
            "created",
            uuid=observed.uuid,
            version=observed.version,
            created_at=observed.created_at,
            updated_at=observed.updated_at,
        )

        self.assertEqual(expected, observed)


if __name__ == "__main__":
    unittest.main()
