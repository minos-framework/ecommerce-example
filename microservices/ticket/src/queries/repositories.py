"""
Copyright (C) 2021 Clariteia SL
This file is part of minos framework.
Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from __future__ import (
    annotations,
)

from typing import (
    NoReturn,
)
from uuid import (
    UUID,
)
from sqlalchemy import (
    and_,
    create_engine,
)
from sqlalchemy.orm import (
    sessionmaker,
)
from minos.common import (
    MinosConfig,
    PostgreSqlMinosDatabase,
)
from .models import (
    META,
    TICKET_TABLE,
    TICKET_ENTRY_TABLE,
)


class TicketQueryRepository(PostgreSqlMinosDatabase):
    """Ticket Amount repository"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = create_engine("postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(**kwargs))
        self.session = sessionmaker(bind=self.engine)()

    async def _setup(self) -> NoReturn:
        META.create_all(self.engine)

    @classmethod
    def _from_config(cls, *args, config: MinosConfig, **kwargs) -> TicketQueryRepository:
        return cls(*args, **(config.repository._asdict() | {"database": "ticket_query_db"}) | kwargs)