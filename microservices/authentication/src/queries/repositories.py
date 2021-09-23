from __future__ import annotations

from typing import NoReturn
from uuid import UUID

from minos.common import (
    MinosConfig,
    MinosSetup,
)
from sqlalchemy import (
    and_,
    create_engine,
)
from sqlalchemy.exc import IntegrityError

from .exceptions import AlreadyExists
from .models import (
    CREDENTIALS_TABLE,
    META,
)


class CredentialsQueryRepository(MinosSetup):
    """ProductInventory Repository class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = create_engine("postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(**kwargs))

    async def _setup(self) -> NoReturn:
        META.create_all(self.engine)

    @classmethod
    def _from_config(cls, *args, config: MinosConfig, **kwargs) -> CredentialsQueryRepository:
        return cls(*args, **(config.repository._asdict() | {"database": "auth_query_db"}) | kwargs)

    async def create_credentials(self, uuid: UUID, username: str, password: str, active: bool) -> None:
        try:
            query = CREDENTIALS_TABLE.insert().values(uuid=uuid, username=username, password=password, active=active)
            self.engine.execute(query)
        except IntegrityError:
            raise AlreadyExists

    async def exist_credentials(self, username, password) -> bool:
        query = CREDENTIALS_TABLE.select().where(
            and_(
                CREDENTIALS_TABLE.columns.username == username,
                CREDENTIALS_TABLE.columns.password == password,
                CREDENTIALS_TABLE.columns.active == True,  # Do not substitute '==' by 'is' # noqa: E712
            )
        )

        return True if self.engine.execute(query).first() else False

    async def get_by_username(self, username: str):
        query = CREDENTIALS_TABLE.select().where(CREDENTIALS_TABLE.columns.username == username)
        return self.engine.execute(query).first()
