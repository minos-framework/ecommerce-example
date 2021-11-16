from __future__ import (
    annotations,
)

import base64
from pathlib import (
    Path,
)
from typing import (
    Optional,
)
from uuid import (
    UUID,
    uuid4,
)

from minos.aggregate import (
    InMemoryEventRepository,
    InMemorySnapshotRepository,
    InMemoryTransactionRepository,
)
from minos.common import (
    CommandReply,
    DependencyInjector,
    Lock,
    MinosBroker,
    MinosConfig,
    MinosPool,
    MinosSagaManager,
    Model,
)
from minos.networks import (
    Request,
    RestRequest,
)
from minos.saga import (
    SagaContext,
)


class _FakeRawRestRequest:
    """For testing purposes"""

    def __init__(self, headers: dict[str, str]):
        self.headers = headers


class _FakeRestRequest(RestRequest):
    """For testing purposes"""

    # noinspection PyMissingConstructor
    def __init__(self, username: str, password: str):
        encoded_credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
        headers = {"Authorization": f"Basic {encoded_credentials}"}
        self.raw_request = _FakeRawRestRequest(headers)


class _FakeRequest(Request):
    """For testing purposes"""

    def __init__(self, content):
        super().__init__()
        self._content = content
        self._user = uuid4()

    @property
    def user(self) -> Optional[UUID]:
        """For testing purposes"""
        return self._user

    async def content(self, **kwargs):
        """For testing purposes"""
        return self._content

    def __eq__(self, other: _FakeRequest) -> bool:
        return self._content == other._content and self.user == other.user

    def __repr__(self) -> str:
        return str()


class _FakeBroker(MinosBroker):
    """For testing purposes."""

    async def send(self, items: list[Model], **kwargs) -> None:
        """For testing purposes."""


class _FakeSagaManager(MinosSagaManager):
    """For testing purposes."""

    async def _run_new(self, name: str, **kwargs) -> UUID:
        """For testing purposes."""

    async def _load_and_run(self, reply: CommandReply, **kwargs) -> UUID:
        """For testing purposes."""


class _FakeSagaExecution:
    def __init__(self, context: SagaContext):
        self.context = context


class FakeLock(Lock):
    """For testing purposes."""

    def __init__(self, key=None, *args, **kwargs):
        if key is None:
            key = "fake"
        super().__init__(key, *args, **kwargs)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return


class FakeLockPool(MinosPool):
    """For testing purposes."""

    async def _create_instance(self):
        return FakeLock()

    async def _destroy_instance(self, instance) -> None:
        """For testing purposes."""


def build_dependency_injector() -> DependencyInjector:
    """For testing purposes"""

    return DependencyInjector(
        build_config(),
        saga_manager=_FakeSagaManager,
        event_broker=_FakeBroker,
        lock_pool=FakeLockPool,
        transaction_repository=InMemoryTransactionRepository,
        event_repository=InMemoryEventRepository,
        snapshot_repository=InMemorySnapshotRepository,
    )


def build_config() -> MinosConfig:
    """For testing purposes"""

    return MinosConfig(DEFAULT_CONFIG_FILE_PATH)


DEFAULT_CONFIG_FILE_PATH = Path(__file__).parents[1] / "config.yml"
