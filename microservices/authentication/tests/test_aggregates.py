import sys
import unittest

from src import (
    Credentials,
)
from tests.utils import (
    build_dependency_injector,
)


class TestCredentials(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.injector = build_dependency_injector()

    async def asyncSetUp(self) -> None:
        self.injector.container.wire(modules=[sys.modules[__name__]])

    async def asyncTearDown(self) -> None:
        self.injector.container.unwire()

    async def test_exists_username(self) -> None:
        self.assertFalse(await Credentials.exists_username("foo"))

        await Credentials.create("foo", "bar", True)

        self.assertTrue(await Credentials.exists_username("foo"))


if __name__ == "__main__":
    unittest.main()
