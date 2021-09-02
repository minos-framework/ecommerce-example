"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""

from dependency_injector.wiring import Provide
from minos.common import AggregateDiff
from minos.cqrs import QueryService
from minos.networks import (
    Request,
    enroute,
)

from .repositories import TicketAmountRepository


class TicketQueryService(QueryService):
    """Ticket Query Service class."""

    repository: TicketAmountRepository = Provide["ticket_amount_repository"]

    @enroute.broker.event("TicketCreated")
    @enroute.broker.event("TicketUpdated")
    async def ticket_created_or_updated(self, request: Request) -> None:
        """Handle the ticket creation events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        uuid = diff.uuid
        total_price = diff["total_price"]

        await self.repository.insert_ticket_amount(uuid, total_price)

    @enroute.broker.event("TicketDeleted")
    async def ticket_deleted(self, request: Request) -> None:
        """Handle the ticket delete events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

        await self.repository.delete(diff.uuid)
