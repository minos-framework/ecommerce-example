from __future__ import (
    annotations,
)

from uuid import (
    UUID,
)

from minos.common import (
    Config,
    DatabaseMixin,
    Injectable,
)
from minos.plugins.aiopg import (
    AiopgDatabaseOperation,
)


@Injectable("payment_amount_repository")
class PaymentAmountRepository(DatabaseMixin):
    """Payment inventory repository"""

    async def _setup(self) -> None:
        operation = AiopgDatabaseOperation(_CREATE_TABLE)
        await self.execute_on_database(operation)

    @classmethod
    def _from_config(cls, *args, config: Config, **kwargs) -> PaymentAmountRepository:
        return cls(*args, **(config.get_default_database() | {"database": "payment_query_db"}) | kwargs)

    async def insert_payment_amount(self, uuid: UUID, amount: int) -> None:
        """ Insert Payment amount
        :param uuid: UUID
        :param amount: Amount in float format
        :return: Nothing
        """
        operation = AiopgDatabaseOperation(_INSERT_PAYMENT_QUERY, {"uuid": uuid, "amount": amount})
        await self.execute_on_database(operation)

    async def delete(self, uuid: UUID) -> None:
        """ Delete Payment
        :param uuid: UUID
        :return: Nothing
        """
        operation = AiopgDatabaseOperation(_DELETE_PAYMENT_QUERY, {"uuid": uuid})
        await self.execute_on_database(operation)


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
