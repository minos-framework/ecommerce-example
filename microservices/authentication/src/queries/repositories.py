from __future__ import (
    annotations,
)

from typing import (
    NoReturn,
)

from minos.common import (
    FieldDiff,
    MinosConfig,
    MinosSetup,
)
from sqlalchemy import (
    create_engine,
)

from .models import (
    META,
)
from .models import USER_TABLE


class UserQueryRepository(MinosSetup):
    """ProductInventory Repository class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = create_engine("postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(**kwargs))

    async def _setup(self) -> NoReturn:
        META.create_all(self.engine)

    @classmethod
    def _from_config(cls, *args, config: MinosConfig, **kwargs) -> UserQueryRepository:
        return cls(*args, **(config.repository._asdict()))

    async def create(self, username: str, password: str, active: bool) -> NoReturn:
        query = USER_TABLE.insert().values(username=username, password=password, active=active)
        self.engine.execute(query)
