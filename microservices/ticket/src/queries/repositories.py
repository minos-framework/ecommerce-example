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

from minos.common import (
    MinosConfig,
    PostgreSqlMinosDatabase,
)


class TicketAmountRepository(PostgreSqlMinosDatabase):
    """Ticket Amount repository"""

    async def _setup(self) -> NoReturn:
        await self.submit_query(_CREATE_TABLE)

    @classmethod
    def _from_config(cls, *args, config: MinosConfig, **kwargs) -> TicketAmountRepository:
        return cls(database="ticket_query_db", port=5432, user="minos", password="min0s", host="localhost")

    async def insert_ticket_amount(self, uuid: UUID, total_price: int) -> NoReturn:
        """ Insert Payment amount
        :param uuid: UUID
        :param total_price: Amount in float format
        :return: Nothing
        """
        await self.submit_query(_INSERT_TICKET_QUERY, {"uuid": uuid, "total_price": total_price})

    async def delete(self, uuid: UUID) -> NoReturn:
        """ Delete Payment
        :param uuid: UUID
        :return: Nothing
        """
        await self.submit_query(_DELETE_TICKET_QUERY, {"uuid": uuid})


_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS ticket (
    uuid UUID NOT NULL PRIMARY KEY,
    total_price FLOAT NOT NULL
);
""".strip()

_INSERT_TICKET_QUERY = """
INSERT INTO ticket (uuid, total_price)
VALUES (%(uuid)s,  %(total_price)s)
ON CONFLICT (uuid)
DO
   UPDATE SET total_price = %(total_price)s
;
""".strip()

_DELETE_TICKET_QUERY = """
DELETE FROM ticket
WHERE uuid = %(uuid)s;
""".strip()
