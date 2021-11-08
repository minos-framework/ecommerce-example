from __future__ import (
    annotations,
)

import sys
import unittest
from pathlib import (
    Path,
)
from uuid import (
    uuid4,
)
from minos.aggregate import (
    InMemoryEventRepository,
    InMemoryTransactionRepository,
    InMemorySnapshotRepository,
)
from minos.common import (
    DependencyInjector,
    MinosConfig,
)
from minos.networks import (
    Response,
)

from src import (
    Customer,
    Product,
    RatingDTO,
    ReviewDTO,
    ReviewQueryRepository,
    ReviewQueryService,
)
from tests.utils import (
    _FakeBroker,
    _FakeRequest,
    _FakeSagaManager, FakeLockPool,
)


class TestReviewQueryService(unittest.IsolatedAsyncioTestCase):
    CONFIG_FILE_PATH = Path(__file__).parents[2] / "config.yml"

    async def asyncSetUp(self) -> None:
        self.config = MinosConfig(self.CONFIG_FILE_PATH)
        self.injector = DependencyInjector(
            self.config,
            saga_manager=_FakeSagaManager,
            event_broker=_FakeBroker,
            lock_pool=FakeLockPool,
            transaction_repository=InMemoryTransactionRepository,
            event_repository=InMemoryEventRepository,
            snapshot_repository=InMemorySnapshotRepository,
            review_repository=ReviewQueryRepository.from_config(self.config, database=self.config.repository.database),
        )
        await self.injector.wire(modules=[sys.modules[__name__]])
        self.service = ReviewQueryService()
        self.repository = self.service.repository

        self.product_1 = Product(uuid=uuid4(), title="Product 1", version=1)
        self.product_2 = Product(uuid=uuid4(), title="Product 2", version=1)
        self.user_1 = Customer(uuid=uuid4(), name="test_user1", version=1)
        self.user_2 = Customer(uuid=uuid4(), name="test_user2", version=1)

        await self._populate_reviews()

    async def asyncTearDown(self) -> None:
        async with self.repository as repository:
            await repository.delete_all()

        await self.injector.unwire()

    async def _populate_reviews(self):

        self.reviews = [
            {
                "uuid": uuid4(),
                "product": self.product_1,
                "user": self.user_1,
                "title": "Review 1",
                "description": "Test 1",
                "score": 2,
                "version": 1,
            },
            {
                "uuid": uuid4(),
                "product": self.product_1,
                "user": self.user_2,
                "title": "Review 2",
                "description": "Test 2",
                "score": 5,
                "version": 1,
            },
            {
                "uuid": uuid4(),
                "product": self.product_2,
                "user": self.user_1,
                "title": "Review 3",
                "description": "Test 3",
                "score": 1,
                "version": 1,
            },
            {
                "uuid": uuid4(),
                "product": self.product_2,
                "user": self.user_2,
                "title": "Review 4",
                "description": "Test 4",
                "score": 3,
                "version": 1,
            },
        ]
        for review in self.reviews:
            async with self.repository as repository:
                await repository.create(**review)

    async def test_get_product_reviews(self):
        request = _FakeRequest({"uuid": self.product_1.uuid})
        response = await self.service.get_product_reviews(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()

        expected = [
            {
                "uuid": self.reviews[0]["uuid"],
                "product_uuid": self.product_1.uuid,
                "user_uuid": self.user_1.uuid,
                "title": self.reviews[0]["title"],
                "description": self.reviews[0]["description"],
                "score": self.reviews[0]["score"],
                "product_title": "Product 1",
                "name": "test_user1",
                "date": observed[0]["date"],
            },
            {
                "uuid": self.reviews[1]["uuid"],
                "product_uuid": self.product_1.uuid,
                "user_uuid": self.user_2.uuid,
                "title": self.reviews[1]["title"],
                "description": self.reviews[1]["description"],
                "score": self.reviews[1]["score"],
                "product_title": "Product 1",
                "name": "test_user2",
                "date": observed[1]["date"],
            },
        ]

        self.assertEqual([ReviewDTO(**row) for row in expected], observed)

    async def test_get_user_reviews(self):
        request = _FakeRequest({"uuid": self.user_1.uuid})
        response = await self.service.get_user_reviews(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()

        expected = [
            {
                "uuid": self.reviews[0]["uuid"],
                "product_uuid": self.product_1.uuid,
                "user_uuid": self.user_1.uuid,
                "title": self.reviews[0]["title"],
                "description": self.reviews[0]["description"],
                "score": self.reviews[0]["score"],
                "product_title": "Product 1",
                "name": "test_user1",
                "date": observed[0]["date"],
            },
            {
                "uuid": self.reviews[2]["uuid"],
                "product_uuid": self.product_2.uuid,
                "user_uuid": self.user_1.uuid,
                "title": self.reviews[2]["title"],
                "description": self.reviews[2]["description"],
                "score": self.reviews[2]["score"],
                "product_title": "Product 2",
                "name": "test_user1",
                "date": observed[1]["date"],
            },
        ]

        self.assertEqual([ReviewDTO(**row) for row in expected], observed)

    async def test_get_product_score_reviews_asc(self):
        request = _FakeRequest({"uuid": self.product_1.uuid, "limit": 1, "order": "asc"})
        response = await self.service.get_product_score_reviews(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()

        expected = [
            {
                "uuid": self.reviews[0]["uuid"],
                "product_uuid": self.product_1.uuid,
                "user_uuid": self.user_1.uuid,
                "title": self.reviews[0]["title"],
                "description": self.reviews[0]["description"],
                "score": self.reviews[0]["score"],
                "product_title": "Product 1",
                "name": "test_user1",
                "date": observed[0]["date"],
            },
        ]

        self.assertEqual([ReviewDTO(**row) for row in expected], observed)

    async def test_get_product_score_reviews_desc(self):
        request = _FakeRequest({"uuid": self.product_1.uuid, "limit": 1, "order": "desc"})
        response = await self.service.get_product_score_reviews(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()

        expected = [
            {
                "uuid": self.reviews[1]["uuid"],
                "product_uuid": self.product_1.uuid,
                "user_uuid": self.user_2.uuid,
                "title": self.reviews[1]["title"],
                "description": self.reviews[1]["description"],
                "score": self.reviews[1]["score"],
                "product_title": "Product 1",
                "name": "test_user2",
                "date": observed[0]["date"],
            },
        ]

        self.assertEqual([ReviewDTO(**row) for row in expected], observed)

    async def test_get_reviews_score_asc(self):
        request = _FakeRequest({"limit": 10, "order": "asc"})
        response = await self.service.get_reviews_score(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()

        expected = [
            {"product_uuid": self.product_2.uuid, "product_title": "Product 2", "average": 2.0},
            {"product_uuid": self.product_1.uuid, "product_title": "Product 1", "average": 3.5},
        ]

        self.assertEqual([RatingDTO(**row) for row in expected], observed)

    async def test_get_reviews_score_desc(self):
        request = _FakeRequest({"limit": 10, "order": "desc"})
        response = await self.service.get_reviews_score(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()

        expected = [
            {"product_uuid": self.product_1.uuid, "product_title": "Product 1", "average": 3.5},
            {"product_uuid": self.product_2.uuid, "product_title": "Product 2", "average": 2.0},
        ]

        self.assertEqual([RatingDTO(**row) for row in expected], observed)

    async def test_get_get_last_reviews(self):
        request = _FakeRequest({"limit": 1})
        response = await self.service.get_last_reviews(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()

        expected = [
            {
                "uuid": self.reviews[3]["uuid"],
                "product_uuid": self.product_2.uuid,
                "user_uuid": self.user_2.uuid,
                "title": self.reviews[3]["title"],
                "description": self.reviews[3]["description"],
                "score": self.reviews[3]["score"],
                "product_title": "Product 2",
                "name": "test_user2",
                "date": observed[0]["date"],
            },
        ]

        self.assertEqual([ReviewDTO(**row) for row in expected], observed)


if __name__ == "__main__":
    unittest.main()
