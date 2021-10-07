import sys
import unittest
from uuid import uuid4

from src import Credentials
from tests.utils import build_dependency_injector


class TestCredentials(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.injector = build_dependency_injector()
        await self.injector.wire(modules=[sys.modules[__name__]])

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_exists_username(self) -> None:
        self.assertFalse(await Credentials.exists_username("foo"))

        await Credentials.create("foo", "bar", True, uuid4())

        self.assertTrue(await Credentials.exists_username("foo"))


if __name__ == "__main__":
    unittest.main()
