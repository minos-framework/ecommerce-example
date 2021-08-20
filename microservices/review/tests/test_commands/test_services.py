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
    Review,
    ReviewCommandService,
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

        self.service = ReviewCommandService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def _create_one_review(self) -> Response:
        request = _FakeRequest(
            {
                "product": "2cc51893-153e-482e-b785-f77c5c1c4aea",
                "user": "e015a2e1-9092-448f-b4ca-a678fc384d0e",
                "title": "Nice package but product broken",
                "description": "The product came nicely packaged but was broken. The seller took care of it and sent me a new one.",
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
            description="The product came nicely packaged but was broken. The seller took care of it and sent me a new one.",
            score=3,
            uuid=observed.uuid,
            version=observed.version,
        )

        self.assertEqual(expected, observed)

    async def test_update_review(self):
        response = await self._create_one_review()

        self.assertIsInstance(response, Response)

        observed = await response.content()

        request = _FakeRequest({"uuid": observed.uuid, "title": "Good product!", "description": "Test.", "score": 5})

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
        )

        self.assertEqual(expected, observed)


if __name__ == "__main__":
    unittest.main()
