from __future__ import (
    annotations,
)

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

from minos.common import (
    CommandReply,
    DependencyInjector,
    InMemoryRepository,
    InMemorySnapshot,
    MinosBroker,
    MinosConfig,
    MinosSagaManager,
    Model,
)
from minos.networks import (
    Request,
)


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


def build_dependency_injector() -> DependencyInjector:
    """For testing purposes"""

    return DependencyInjector(
        build_config(),
        saga_manager=_FakeSagaManager,
        event_broker=_FakeBroker,
        repository=InMemoryRepository,
        snapshot=InMemorySnapshot,
    )


def build_config() -> MinosConfig:
    """For testing purposes"""

    return MinosConfig(DEFAULT_CONFIG_FILE_PATH)


DEFAULT_CONFIG_FILE_PATH = Path(__file__).parents[1] / "config.yml"
