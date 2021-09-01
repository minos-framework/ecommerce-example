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
    NoReturn,
    Optional,
)
from unittest.mock import (
    MagicMock,
    call,
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
from minos.saga import (
    SagaContext,
)
from src import (
    OrderCommandService,
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

        self.service = OrderCommandService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_create_order(self):
        expected = uuid4()

        async def _fn(*args, **kwargs):
            return expected

        mock = MagicMock(side_effect=_fn)
        self.service.saga_manager._run_new = mock

        cart_uuid = uuid4()
        user = uuid4()
        order = uuid4()
        payment_detail = {
            "card_holder": "John",
            "card_number": 2424242424242424,
            "card_expire": "12/24",
            "card_cvc": "123",
        }

        request = _FakeRequest(
            {
                "cart": cart_uuid,
                "user": user,
                "payment": payment_detail,
                "shipment": {
                    "name": "Jack",
                    "last_name": "Johnson",
                    "email": "jack@gmail.com",
                    "address": "Calle Gran Víia 34",
                    "country": "Spain",
                    "city": "Madrid",
                    "province": "Madrid",
                    "zip": 34324,
                },
            }
        )
        response = await self.service.create_order(request)
        self.assertIsInstance(response, Response)

        observed = await response.content()
        self.assertEqual(expected, observed)

        self.assertEqual(expected, observed)
        self.assertEqual(
            call(
                "CreateOrder",
                context=SagaContext(cart_uuid=cart_uuid, order_uuid=order, payment_detail=payment_detail),
                pause_on_disk=True,
                return_execution=False,
            ),
            mock.call_args,
        )


if __name__ == "__main__":
    unittest.main()
