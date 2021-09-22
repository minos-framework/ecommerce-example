from __future__ import (
    annotations,
)

import sys
import unittest
from uuid import (
    uuid4,
)

from minos.networks import (
    Response,
)

from src import (
    Ticket,
    TicketCommandService,
)
from tests.utils import (
    _FakeRequest,
    build_dependency_injector,
)


class TestTicketQueryService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.injector = build_dependency_injector()

        await self.injector.wire(modules=[sys.modules[__name__]])

        self.service = TicketCommandService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def _test_create_ticket(self):
        gen_uuid = [uuid4(), uuid4(), uuid4()]
        request = _FakeRequest({"product_uuids": gen_uuid})
        response = await self.service.create_ticket(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()
        expected = Ticket(
            observed.code,
            [],
            0.0,
            uuid=observed.uuid,
            version=observed.version,
            created_at=observed.created_at,
            updated_at=observed.updated_at,
        )

        self.assertEqual(expected, observed)


if __name__ == "__main__":
    unittest.main()
