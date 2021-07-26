"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""

from minos.cqrs import QueryService
from minos.networks import (
    enroute,
    Request,
)


class OrderQueryService(QueryService):
    """TODO"""

    @enroute.broker.event("OrderCreated")
    async def order_created(self, request: Request):
        """TODO

        :param request: TODO
        :return: TODO
        """
        print(await request.content())

    @enroute.broker.event("OrderUpdated")
    async def order_updated(self, request: Request):
        """TODO

        :param request: TODO
        :return: TODO
        """
        print(await request.content())

    @enroute.broker.event("OrderDeleted")
    async def order_deleted(self, request: Request):
        """TODO

        :param request: TODO
        :return: TODO
        """
        print(await request.content())
