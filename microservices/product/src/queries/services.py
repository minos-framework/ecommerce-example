"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import (
    NoReturn,
)

from dependency_injector.wiring import (
    Provide,
)
from minos.common import (
    AggregateDiff,
)
from minos.cqrs import (
    QueryService,
)
from minos.networks import (
    Request,
    Response,
    ResponseException,
    enroute,
)

from .repositories import (
    ProductRepository,
)


class ProductQueryService(QueryService):
    """Product Query Service class."""

    repository: ProductRepository = Provide["product_repository"]

    # noinspection PyUnusedLocal
    @enroute.rest.query("/products/without-stock", "GET")
    @enroute.broker.query("GetProductsWithoutStock")
    async def get_products_without_stock(self, request: Request) -> Response:
        """Get the products without stock.

        :param request: A request without any content.
        :return: A response containing the products without stock.
        """
        uuids = await self.repository.get_without_stock()
        return Response(uuids)

    @enroute.broker.query("GetMostSoldProducts")
    def get_most_sold_products(self, request: Request) -> Response:
        """Get the most sold products.

        :param request: A request containing the maximum number of products to be retrieved.
        :return: A response containing the most sold products.
        """
        raise ResponseException("Not Implemented yet!")

    @enroute.broker.event("ProductCreated")
    @enroute.broker.event("ProductUpdated")
    async def product_created_or_updated(self, request: Request) -> NoReturn:
        """Handle the product create and update events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

        uuid = diff.uuid

        if "inventory" not in diff.fields_diff.keys():
            return

        inventory_amount = diff.fields_diff["inventory"].amount

        await self.repository.insert_inventory_amount(uuid, inventory_amount)

    @enroute.broker.event("ProductDeleted")
    async def product_deleted(self, request: Request) -> NoReturn:
        """Handle the product delete events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

        await self.repository.delete(diff.uuid)
