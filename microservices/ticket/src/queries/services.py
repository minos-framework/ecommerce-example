"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import NoReturn

import aiopg
from minos.common import AggregateDiff
from minos.cqrs import QueryService
from minos.networks import (
    Request,
    enroute,
)

from src.queries.repositories import TicketAmountRepository


class TicketQueryService(QueryService):
    """Ticket Query Service class."""

    @enroute.broker.event("TicketCreated")
    @enroute.broker.event("TicketUpdated")
    async def ticket_created_or_updated(self, request: Request) -> NoReturn:
        """Handle the ticket creation events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        uuid = diff.uuid
        total_price = diff.fields_diff["total_price"]

        async with TicketAmountRepository.from_config(config=self.config) as repository:
            await repository.insert_ticket_amount(uuid, total_price)

    @enroute.broker.event("TicketDeleted")
    async def ticket_deleted(self, request: Request) -> NoReturn:
        """Handle the ticket delete events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

        async with TicketAmountRepository.from_config(config=self.config) as repository:
            await repository.delete(diff.uuid)
