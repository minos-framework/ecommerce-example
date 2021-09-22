import sys
import unittest

from tests.utils import (
    build_dependency_injector,
)


class TestAuthentication(unittest.IsolatedAsyncioTestCase):
    """Test Order"""

    def setUp(self) -> None:
        self.injector = build_dependency_injector()

    async def asyncSetUp(self) -> None:
        await self.injector.wire(modules=[sys.modules[__name__]])

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()


if __name__ == "__main__":
    unittest.main()
