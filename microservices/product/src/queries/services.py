"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import NoReturn

from minos.common import (
    Event,
    Request,
    Response,
    Service,
)


class ProductQueryService(Service):
    """TODO"""

    def get_products_without_stock(self, request: Request) -> Response:
        """TODO

        :return: TODO
        """

    def get_most_sold_products(self, request: Request) -> Response:
        """TODO

        :return: TODO
        """

    # @subscribe("ProductAdded")
    async def product_created(self, topic: str, event: Event) -> NoReturn:
        """TODO

        :param topic: TODO
        :param event: TODO
        :return: TODO
        """
        diff = event.data
        print(topic, diff)

    # @subscribe("ProductUpdated")
    async def product_updated(self, topic: str, event: Event) -> NoReturn:
        """TODO

        :param topic: TODO
        :param event: TODO
        :return: TODO
        """
        diff = event.data
        print(topic, diff)

    # @subscribe("ProductDeleted")
    async def product_deleted(self, topic: str, event: Event) -> NoReturn:
        """TODO

        :param topic: TODO
        :param event: TODO
        :return: TODO
        """
        diff = event.data
        print(topic, diff)
