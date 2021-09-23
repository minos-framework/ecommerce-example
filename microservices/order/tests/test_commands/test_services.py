from __future__ import annotations

import sys
import unittest

from tests.utils import build_dependency_injector


class TestOrderCommandService(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.injector = build_dependency_injector()

    async def asyncSetUp(self) -> None:
        await self.injector.wire(modules=[sys.modules[__name__]])

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_true(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
