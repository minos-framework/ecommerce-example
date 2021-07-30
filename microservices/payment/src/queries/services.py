"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import NoReturn

from minos.common import AggregateDiff
from minos.cqrs import QueryService
from minos.networks import (
    Request,
    enroute,
)
from src.queries.repositories import PaymentAmountRepository
from dependency_injector.wiring import Provide


class PaymentQueryService(QueryService):
    """Payment Query Service class"""

    repository: PaymentAmountRepository = Provide["payment_amount_repository"]

    @enroute.broker.event("PaymentCreated")
    @enroute.broker.event("PaymentUpdated")
    async def payment_created_or_updated(self, request: Request) -> NoReturn:
        """Handle the payment create events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        uuid = diff.uuid
        amount = diff.fields_diff["amount"]

        await self.repository.insert_payment_amount(uuid, amount)

    @enroute.broker.event("PaymentDeleted")
    async def payment_deleted(self, request: Request) -> NoReturn:
        """Handle the payment delete events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

        await self.repository.delete(diff.uuid)
