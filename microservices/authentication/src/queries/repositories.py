from __future__ import (
    annotations,
)

from typing import (
    NoReturn,
)
from uuid import (
    UUID,
)

from minos.common import (
    MinosConfig,
    MinosSetup,
)
from sqlalchemy import (
    and_,
    create_engine,
)
from sqlalchemy.exc import (
    IntegrityError,
)

from .exceptions import (
    AlreadyExists,
)
from .models import (
    META,
    USER_TABLE,
)


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

    async def create_user(self, uuid: UUID, username: str, password: str, active: bool) -> None:
        try:
            query = USER_TABLE.insert().values(uuid=uuid, username=username, password=password, active=active)
            self.engine.execute(query)
        except IntegrityError:
            raise AlreadyExists

    async def exist_credentials(self, username, password) -> bool:
        query = USER_TABLE.select().where(
            and_(
                USER_TABLE.columns.username == username,
                USER_TABLE.columns.password == password,
                USER_TABLE.columns.active == True,  # Do not substitute '==' by 'is'
            )
        )

        return True if self.engine.execute(query).first() else False

    async def get_by_username(self, username: str):
        query = USER_TABLE.select().where(USER_TABLE.columns.username == username)
        return self.engine.execute(query).first()
