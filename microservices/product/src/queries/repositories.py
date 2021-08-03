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


class ProductInventoryRepository(PostgreSqlMinosDatabase):
    """ProductInventory Repository class."""

    async def _setup(self) -> NoReturn:
        await self.submit_query(_CREATE_TABLE)

    @classmethod
    def _from_config(cls, *args, config: MinosConfig, **kwargs) -> ProductInventoryRepository:
        return cls(*args, **(config.repository._asdict() | {"database": "product_query_db"}) | kwargs)

    async def get_without_stock(self) -> list[UUID]:
        """Get product identifiers that do not have stock.

        :return: A list of UUID values.
        """
        entries = [entry async for entry in self.submit_query_and_iter(_GET_PRODUCTS_WITHOUT_STOCK)]
        uuids = [entry[0] for entry in entries]
        return uuids

    async def insert_inventory_amount(self, uuid: UUID, inventory_amount: int) -> NoReturn:
        """Insert inventory values on the database.

        :param uuid: The product identifier.
        :param inventory_amount: The amount.
        :return: This method does not return anything.
        """
        await self.submit_query(_INSERT_PRODUCT_QUERY, {"uuid": uuid, "inventory_amount": inventory_amount})

    async def delete(self, uuid: UUID) -> NoReturn:
        """Delete an entry from the database.

        :param uuid: The product identifier.
        :return: This method does not return anything.
        """
        await self.submit_query(_DELETE_PRODUCT_QUERY, {"uuid": uuid})


_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS product (
    uuid UUID NOT NULL PRIMARY KEY,
    inventory_amount INT NOT NULL
);
""".strip()

_INSERT_PRODUCT_QUERY = """
INSERT INTO product (uuid, inventory_amount)
VALUES (%(uuid)s,  %(inventory_amount)s)
ON CONFLICT (uuid)
DO
   UPDATE SET inventory_amount = %(inventory_amount)s
;
""".strip()

_DELETE_PRODUCT_QUERY = """
DELETE FROM product
WHERE uuid = %(uuid)s;
""".strip()

_GET_PRODUCTS_WITHOUT_STOCK = """
SELECT uuid 
FROM product
WHERE inventory_amount = 0;
""".strip()
