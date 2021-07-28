"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from __future__ import annotations

import sys
import unittest
from asyncio import gather
from pathlib import Path
from typing import NoReturn
from uuid import UUID

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
    Payment,
    PaymentCommandService,
)


class _FakeRequest(Request):
    """For testing purposes"""

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


class TestOrderCommandService(unittest.IsolatedAsyncioTestCase):
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

        self.service = PaymentCommandService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_create_order(self):
        request = _FakeRequest({"credit_number": 1234, "amount": 3.4})
        response = await self.service.create_payment(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()
        expected = Payment(1234, 3.4, "created", uuid=observed.uuid, version=observed.version)

        self.assertEqual(expected, observed)

    async def test_get_payments(self):
        expected = await gather(Payment.create(1234, 3.4, "created"), Payment.create(5678, 3.4, "cancelled"),)

        request = _FakeRequest({"uuids": [v.uuid for v in expected]})

        response = await self.service.get_payments(request)
        observed = await response.content()

        self.assertEqual(expected, observed)


if __name__ == "__main__":
    unittest.main()
