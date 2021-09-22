from __future__ import annotations

import sys
import unittest

from src import CartQueryService
from tests.utils import build_dependency_injector


class TestCartQueryService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.injector = build_dependency_injector()
        await self.injector.wire(modules=[sys.modules[__name__]])

        self.service = CartQueryService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()


if __name__ == "__main__":
    unittest.main()
