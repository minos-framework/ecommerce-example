"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import (
    NoReturn,
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

    @enroute.broker.query("GetProductsWithoutStock")
    def get_products_without_stock(self, request: Request) -> Response:
        """TODO

        :param request: TODO
        :return: TODO
        """

    @enroute.broker.query("GetMostSoldProducts")
    def get_most_sold_products(self, request: Request) -> Response:
        """TODO

        :param request: TODO
        :return: TODO
        """

    @staticmethod
    @enroute.broker.event("ProductAdded")
    async def product_created(request: Request) -> NoReturn:
        """TODO

        :param request: TODO
        :return: TODO
        """
        print(await request.content())

    @staticmethod
    @enroute.broker.event("ProductUpdated")
    async def product_updated(request: Request) -> NoReturn:
        """TODO

        :param request: TODO
        :return: TODO
        """
        print(await request.content())

    @staticmethod
    @enroute.broker.event("ProductDeleted")
    async def product_deleted(request: Request) -> NoReturn:
        """TODO

        :param request: TODO
        :return: TODO
        """
        print(await request.content())
