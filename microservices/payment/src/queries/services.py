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


class PaymentQueryService(QueryService):
    """Payment Query Service class"""

    @enroute.broker.event("PaymentCreated")
    @enroute.broker.event("PaymentUpdated")
    async def payment_created_or_updated(self, request: Request) -> NoReturn:
        """Handle the payment create events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        uuid = diff.uuid
        amount = diff.fields_diff["amount"]

        async with await self._get_connection() as connection:
            await self._create_table(connection)
            async with connection.cursor() as cursor:
                await cursor.execute(_INSERT_PAYMENT_QUERY, {"uuid": uuid, "amount": amount})

    @enroute.broker.event("PaymentDeleted")
    async def payment_deleted(self, request: Request) -> NoReturn:
        """Handle the payment delete events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

        async with await self._get_connection() as connection:
            await self._create_table(connection)
            async with connection.cursor() as cursor:
                await cursor.execute(_DELETE_PAYMENT_QUERY, {"uuid": diff.uuid})

    @staticmethod
    async def _get_connection():
        return await aiopg.connect(database="payment_query_db", user="minos", password="min0s", host="localhost")

    async def _create_table(self, connection):
        async with connection.cursor() as cursor:
            await cursor.execute(_CREATE_TABLE)


_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS payment (
    uuid UUID NOT NULL PRIMARY KEY,
    amount FLOAT NOT NULL
);
""".strip()

_INSERT_PAYMENT_QUERY = """
INSERT INTO payment (uuid, amount)
VALUES (%(uuid)s,  %(amount)s)
ON CONFLICT (uuid)
DO
   UPDATE SET amount = %(amount)s
;
""".strip()

_DELETE_PAYMENT_QUERY = """
DELETE FROM payment
WHERE uuid = %(uuid)s;
""".strip()
