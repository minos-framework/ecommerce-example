"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
import sys
import unittest.async_case
from asyncio import (
    gather,
)
from pathlib import (
    Path,
)
from typing import (
    NoReturn,
)
from uuid import (
    UUID,
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
    Request,
    Response,
)
from src import (
    Inventory,
    InventoryController,
    InventoryService,
)


class _FakeRequest(Request):
    """For testing purposes"""

    def __init__(self, content):
        super().__init__()
        self._content = content

    async def content(self):
        """For testing purposes"""
        return self._content


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


class TestInventoryController(unittest.IsolatedAsyncioTestCase):
    CONFIG_FILE_PATH = Path(__file__).parents[1] / "config.yml"

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

        self.controller = InventoryController()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_create_inventories(self):
        request = _FakeRequest([{"product": 1, "amount": 34}])
        response = await self.controller.create_inventory(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()
        self.assertEqual(1, len(observed))
        self.assertEqual(Inventory(1, 34, id=observed[0].id, version=observed[0].version), observed[0])

    async def test_get_inventorys(self):
        service = InventoryService()
        expected = await gather(
            service.create_inventory(1, 34),
            service.create_inventory(2, 12),
            service.create_inventory(3, 43),
        )
        ids = [v.id for v in expected]
        request = _FakeRequest(ids)

        response = await self.controller.get_inventories(request)
        observed = await response.content()
        self.assertEqual(expected, observed)


if __name__ == "__main__":
    unittest.main()
