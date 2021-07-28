"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.cqrs import QueryService
from minos.networks import (
    Request,
    enroute,
)
from typing import NoReturn


class TicketQueryService(QueryService):
    """Ticket Query Service class."""

    @enroute.broker.event("TicketAdded")
    async def ticket_created(self, request: Request) -> NoReturn:
        """Handle the ticket creation events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        print(await request.content())

    @enroute.broker.event("TicketUpdated")
    async def ticket_updated(self, request: Request) -> NoReturn:
        """Handle the ticket update events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        print(await request.content())

    @enroute.broker.event("TicketDeleted")
    async def ticket_deleted(self, request: Request) -> NoReturn:
        """Handle the ticket delete events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        print(await request.content())
