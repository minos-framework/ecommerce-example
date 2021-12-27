from __future__ import (
    annotations,
)

import sys
import unittest

from minos.aggregate import (
    EntitySet,
)
from minos.networks import (
    InMemoryRequest,
    Response,
)

from src import (
    Cart,
    CartCommandService,
)
from tests.utils import (
    build_dependency_injector,
)


class TestCartCommandService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.injector = build_dependency_injector()
        await self.injector.wire(modules=[sys.modules[__name__]])

        self.service = CartCommandService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_create_cart(self):
        request = InMemoryRequest({"user": 3})
        response = await self.service.create_cart(request)

        self.assertIsInstance(response, Response)
        observed = await response.content()
        expected = Cart(
            3,
            EntitySet({}),
            uuid=observed.uuid,
            version=observed.version,
            created_at=observed.created_at,
            updated_at=observed.updated_at,
        )

        self.assertEqual(expected, observed)


if __name__ == "__main__":
    unittest.main()
