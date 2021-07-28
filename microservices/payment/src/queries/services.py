"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import NoReturn

from minos.cqrs import QueryService
from minos.networks import (
    Request,
    enroute,
)


class PaymentQueryService(QueryService):
    """TODO"""

    @staticmethod
    @enroute.broker.event("PaymentCreated")
    async def payment_created(request: Request) -> NoReturn:
        """Handle the payment create events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        print(await request.content())

    @staticmethod
    @enroute.broker.event("PaymentUpdated")
    async def payment_updated(request: Request) -> NoReturn:
        """Handle the payment update events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        print(await request.content())

    @staticmethod
    @enroute.broker.event("PaymentDeleted")
    async def payment_deleted(request: Request) -> NoReturn:
        """Handle the payment delete events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        print(await request.content())
