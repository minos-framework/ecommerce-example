"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import (
    NoReturn,
)
from minos.common import (
    AggregateDiff,
)
from minos.cqrs import (
    QueryService,
)
from minos.networks import (
    Request,
    enroute,
)
import aiopg


class TicketQueryService(QueryService):
    """Ticket Query Service class."""

    @enroute.broker.event("TicketCreated")
    @enroute.broker.event("TicketUpdated")
    async def ticket_created_or_updated(self, request: Request) -> NoReturn:
        """Handle the ticket creation events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        """Handle the product create and update events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        uuid = diff.uuid
        total_price = diff.fields_diff["total_price"]

        async with await self._get_connection() as connection:
            await self._create_table(connection)
            async with connection.cursor() as cursor:
                await cursor.execute(_INSERT_TICKET_QUERY, {"uuid": uuid, "total_price": total_price})

    @enroute.broker.event("TicketDeleted")
    async def ticket_deleted(self, request: Request) -> NoReturn:
        """Handle the ticket delete events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

        async with await self._get_connection() as connection:
            await self._create_table(connection)
            async with connection.cursor() as cursor:
                await cursor.execute(_DELETE_TICKET_QUERY, {"uuid": diff.uuid})

    @staticmethod
    async def _get_connection():
        return await aiopg.connect(database="ticket_query_db", user="minos", password="min0s", host="localhost")

    async def _create_table(self, connection):
        async with connection.cursor() as cursor:
            await cursor.execute(_CREATE_TABLE)


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
