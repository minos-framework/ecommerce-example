from __future__ import (
    annotations,
)

import sys
import unittest
from uuid import (
    UUID,
)

from minos.aggregate import (
    EntitySet,
)

from src import (
    Ticket,
    TicketQueryService,
)
from tests.utils import (
    build_dependency_injector,
)


class TestTicketQueryService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.injector = build_dependency_injector()
        await self.injector.wire(modules=[sys.modules[__name__]])

        self.service = TicketQueryService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_get_payments(self):
        expected = await Ticket.create("kokrte3432", 1.4, EntitySet())

        # request = _FakeRequest({"uuid": expected.uuid})

        # response = await self.service.get_ticket(request)
        # observed = await response.content()

        self.assertIsInstance(expected.uuid, UUID)


if __name__ == "__main__":
    unittest.main()
