"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import (
    NoReturn,
)

import aiopg
from minos.common import (
    AggregateDiff,
)
from minos.cqrs import (
    QueryService,
)
from minos.networks import (
    Request,
    Response,
    enroute,
)


class ProductQueryService(QueryService):
    """Product Query Service class."""

    # noinspection PyUnusedLocal
    @enroute.rest.query("/products/without-stock", "GET")
    @enroute.broker.query("GetProductsWithoutStock")
    async def get_products_without_stock(self, request: Request) -> Response:
        """Get the products without stock.

        :param request: A request without any content.
        :return: A response containing the products without stock.
        """
        async with await self._get_connection() as connection:
            await self._create_table(connection)
            async with connection.cursor() as cursor:
                await cursor.execute(_GET_PRODUCTS_WITHOUT_STOCK)
                entries = await cursor.fetchall()

        uuids = [entry[0] for entry in entries]
        return Response(uuids)

    @enroute.broker.query("GetMostSoldProducts")
    def get_most_sold_products(self, request: Request) -> Response:
        """Get the most sold products.

        :param request: A request containing the maximum number of products to be retrieved.
        :return: A response containing the most sold products.
        """

    @enroute.broker.event("ProductCreated")
    @enroute.broker.event("ProductUpdated")
    async def product_created_or_updated(self, request: Request) -> NoReturn:
        """Handle the product create and update events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        uuid = diff.uuid
        inventory_amount = diff.fields_diff["inventory"].amount

        async with await self._get_connection() as connection:
            await self._create_table(connection)
            async with connection.cursor() as cursor:
                await cursor.execute(_INSERT_PRODUCT_QUERY, {"uuid": uuid, "inventory_amount": inventory_amount})

    @enroute.broker.event("ProductDeleted")
    async def product_deleted(self, request: Request) -> NoReturn:
        """Handle the product delete events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

        async with await self._get_connection() as connection:
            await self._create_table(connection)
            async with connection.cursor() as cursor:
                await cursor.execute(_DELETE_PRODUCT_QUERY, {"uuid": diff.uuid})

    @staticmethod
    async def _get_connection():
        return await aiopg.connect(database="product_query_db", user="minos", password="min0s", host="localhost")

    async def _create_table(self, connection):
        async with connection.cursor() as cursor:
            await cursor.execute(_CREATE_TABLE)


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
