"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import NoReturn

from minos.cqrs import QueryService
from minos.networks import (
    Request,
    Response,
    enroute,
)


class ProductQueryService(QueryService):
    """Product Query Service class."""

    @enroute.broker.query("GetProductsWithoutStock")
    def get_products_without_stock(self, request: Request) -> Response:
        """Get the products without stock.

        :param request: A request without any content.
        :return: A response containing the products without stock.
        """

    @enroute.broker.query("GetMostSoldProducts")
    def get_most_sold_products(self, request: Request) -> Response:
        """Get the most sold products.

        :param request: A request containing the maximum number of products to be retrieved.
        :return: A response containing the most sold products.
        """

    @staticmethod
    @enroute.broker.event("ProductAdded")
    async def product_created(request: Request) -> NoReturn:
        """Handle the product create events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        print(await request.content())

    @staticmethod
    @enroute.broker.event("ProductUpdated")
    async def product_updated(request: Request) -> NoReturn:
        """Handle the product update events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        print(await request.content())

    @staticmethod
    @enroute.broker.event("ProductDeleted")
    async def product_deleted(request: Request) -> NoReturn:
        """Handle the product delete events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        print(await request.content())
