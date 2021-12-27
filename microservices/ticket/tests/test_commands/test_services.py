from __future__ import (
    annotations,
)

import sys
import unittest
from unittest.mock import (
    AsyncMock,
)
from uuid import (
    uuid4,
)

from minos.networks import (
    InMemoryRequest,
    Response,
)
from minos.saga import (
    SagaContext,
)

from src import (
    Ticket,
    TicketCommandService,
)
from tests.utils import (
    _FakeSagaExecution,
    build_dependency_injector,
)


class TestTicketCommandService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.injector = build_dependency_injector()

        await self.injector.wire(modules=[sys.modules[__name__]])

        self.service = TicketCommandService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_create_ticket(self):
        gen_uuid = [uuid4(), uuid4(), uuid4()]
        request = InMemoryRequest({"cart_uuid": gen_uuid})

        expected = await Ticket.create("test", 0.0, [])

        self.injector.saga_manager.run = AsyncMock(return_value=_FakeSagaExecution(SagaContext(ticket=expected)))

        response = await self.service.create_ticket(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()
        self.assertEqual(expected, observed)


if __name__ == "__main__":
    unittest.main()
