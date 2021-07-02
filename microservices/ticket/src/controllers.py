"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import (
    Request,
    Response,
)

from .services import (
    TicketService,
)


class TicketController:
    """Ticket Controller class"""

    @staticmethod
    async def create_ticket(request: Request) -> Response:
        """Create a new ticket.

        :param request: The ``Request`` instance to be use to compute the price.
        :return: A ``Response`` containing the created ticket.
        """
        content = await request.content()
        ticket = await TicketService().create_ticket(**content)
        return Response(ticket)

    @staticmethod
    async def get_tickets(request: Request) -> Response:
        """Get a list of tickets by id.

        :param request: A ``Request`` instance containing the list of ticket identifiers.
        :return: A ``Response`` containing the list of requested tickets.
        """
        content = await request.content()
        if isinstance(content["ids"], list):
            ids = list(map(int, content["ids"]))
        else:
            ids = [int(content["ids"])]
        tickets = await TicketService().get_tickets(ids)
        return Response(tickets)
