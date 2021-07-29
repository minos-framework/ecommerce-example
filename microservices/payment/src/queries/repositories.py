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


class PaymentAmountRepository(PostgreSqlMinosDatabase):
    """Payment inventory repository"""

    async def _setup(self) -> NoReturn:
        await self.submit_query(_CREATE_TABLE)

    @classmethod
    def _from_config(cls, *args, config: MinosConfig, **kwargs) -> PaymentAmountRepository:
        return cls(database="payment_query_db", port=5432, user="minos", password="min0s", host="localhost")

    async def insert_payment_amount(self, uuid: UUID, amount: int) -> NoReturn:
        """ Insert Payment amount
        :param uuid: UUID
        :param amount: Amount in float format
        :return: Nothing
        """
        await self.submit_query(_INSERT_PAYMENT_QUERY, {"uuid": uuid, "amount": amount})

    async def delete(self, uuid: UUID) -> NoReturn:
        """ Delete Payment
        :param uuid: UUID
        :return: Nothing
        """
        await self.submit_query(_INSERT_PAYMENT_QUERY, {"uuid": uuid})


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
