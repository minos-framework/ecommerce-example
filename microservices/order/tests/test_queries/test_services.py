from __future__ import annotations

import sys
import unittest
from pathlib import Path

from tests.utils import build_dependency_injector


class TestOrderQueryService(unittest.IsolatedAsyncioTestCase):
    CONFIG_FILE_PATH = Path(__file__).parents[2] / "config.yml"

    def setUp(self) -> None:
        self.injector = build_dependency_injector()

    async def asyncSetUp(self) -> None:
        await self.injector.wire(modules=[sys.modules[__name__]])

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()


if __name__ == "__main__":
    unittest.main()
