from __future__ import annotations

import sys
import unittest

from minos.networks import (
    InMemoryRequest,
    Response,
)

from src import (
    Review,
    ReviewCommandService,
)
from tests.utils import build_dependency_injector


class TestProductCommandService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.injector = build_dependency_injector()

        await self.injector.wire(modules=[sys.modules[__name__]])

        self.service = ReviewCommandService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def _create_one_review(self) -> Response:
        request = InMemoryRequest(
            {
                "product": "2cc51893-153e-482e-b785-f77c5c1c4aea",
                "user": "e015a2e1-9092-448f-b4ca-a678fc384d0e",
                "title": "Nice package but product broken",
                "description": (
                    "The product came nicely packaged but was broken. The seller took care of it and sent me a new one."
                ),
                "score": 3,
            }
        )
        response = await self.service.create_review(request)

        return response

    async def test_create_review(self):
        response = await self._create_one_review()

        self.assertIsInstance(response, Response)

        observed = await response.content()
        expected = Review(
            product=observed.product,
            user=observed.user,
            title="Nice package but product broken",
            description=(
                "The product came nicely packaged but was broken. The seller took care of it and sent me a new one."
            ),
            score=3,
            uuid=observed.uuid,
            version=observed.version,
            created_at=observed.created_at,
            updated_at=observed.updated_at,
        )

        self.assertEqual(expected, observed)

    async def test_update_review(self):
        response = await self._create_one_review()

        self.assertIsInstance(response, Response)

        observed = await response.content()

        request = InMemoryRequest({"uuid": observed.uuid, "title": "Good product!", "description": "Test.", "score": 5})

        response = await self.service.update_review(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()

        expected = Review(
            product=observed.product,
            user=observed.user,
            title="Good product!",
            description="Test.",
            score=5,
            uuid=observed.uuid,
            version=observed.version,
            created_at=observed.created_at,
            updated_at=observed.updated_at,
        )

        self.assertEqual(expected, observed)


if __name__ == "__main__":
    unittest.main()
