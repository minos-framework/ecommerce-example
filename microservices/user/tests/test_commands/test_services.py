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
from pathlib import (
    Path,
)
from typing import (
    NoReturn, Optional,
)
from uuid import (
    UUID,
    uuid4,
)
from datetime import (
    datetime,
)
from minos.common import (
    CommandReply,
    DependencyInjector,
    InMemoryRepository,
    InMemorySnapshot,
    MinosBroker,
    MinosConfig,
    MinosSagaManager,
    Model, ValueObjectSet, ValueObject,
)
from cached_property import (
    cached_property,
)
from minos.networks import (
    Request,
    Response,
)
from src import (
    Address,
    User,
    UserCommandService,
)
from src.aggregates import CreditCard


class _FakeRequest(Request):
    """For testing purposes"""

    @cached_property
    def user(self) -> Optional[UUID]:
        """For testing purposes"""
        return uuid4()

    def __init__(self, content):
        super().__init__()
        self._content = content

    async def content(self, **kwargs):
        """For testing purposes"""
        return self._content

    def __eq__(self, other: _FakeRequest) -> bool:
        return self._content == other._content

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


class TestUserCommandService(unittest.IsolatedAsyncioTestCase):
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

        self.service = UserCommandService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_create_user(self):
        request = _FakeRequest(
            {
                "username": "john_coltrane",
                "password": "john_pass",
                "status": "created",
                "address": {"street": "Green Dolphin Street", "street_no": 42},
            }
        )
        response = await self.service.create_user(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()

        credit_cards = ValueObjectSet()
        expected = User(
            username="john_coltrane",
            password="john_pass",
            status="created",
            created_at=observed.created_at,
            address=Address(street="Green Dolphin Street", street_no=42),
            credit_cards=credit_cards,
            uuid=observed.uuid,
            version=observed.version,
        )

        self.assertEqual(expected, observed)

    async def test_add_credit_cart(self):
        request = _FakeRequest(
            {
                "username": "john_coltrane",
                "password": "john_pass",
                "status": "created",
                "address": {"street": "Green Dolphin Street", "street_no": 42},
            }
        )
        response = await self.service.create_user(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()

        credit_cards = ValueObjectSet()
        expected = User(
            username="john_coltrane",
            password="john_pass",
            status="created",
            created_at=observed.created_at,
            address=Address(street="Green Dolphin Street", street_no=42),
            credit_cards=credit_cards,
            uuid=observed.uuid,
            version=observed.version,
        )

        self.assertEqual(expected, observed)

        request = _FakeRequest(
            {
                "name": "Example credit cart",
                "uuid": observed.uuid
            }
        )
        response = await self.service.add_credit_card(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()
        credit_card = CreditCard(name="Example credit cart")
        credit_cards = ValueObjectSet()
        credit_cards.add(credit_card)
        expected = User(
            username="john_coltrane",
            password="john_pass",
            status="created",
            created_at=observed.created_at,
            address=Address(street="Green Dolphin Street", street_no=42),
            credit_cards=credit_cards,
            uuid=observed.uuid,
            version=observed.version,
        )

        self.assertEqual(expected, observed)


if __name__ == "__main__":
    unittest.main()
