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
    enroute,
)


class OrderQueryService(QueryService):
    """Order Query Service class."""

    @enroute.broker.event("OrderCreated")
    async def order_created(self, request: Request) -> NoReturn:
        """Handle the order creation events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        print(await request.content())

    @enroute.broker.event("OrderUpdated")
    async def order_updated(self, request: Request) -> NoReturn:
        """Handle the order update events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        print(await request.content())

    @enroute.broker.event("OrderDeleted")
    async def order_deleted(self, request: Request) -> NoReturn:
        """Handle the order deletion events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        print(await request.content())
