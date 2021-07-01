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
        """TODO

        :param request:TODO
        :return: TODO
        """
        content = await request.content()
        ticket = await TicketService().create_ticket(**content)
        return Response(ticket)

    @staticmethod
    async def get_tickets(request: Request) -> Response:
        """TODO

        :param request: TODO
        :return: TODO
        """
        content = await request.content()
        ids = list(map(int, content["ids"]))
        tickets = await TicketService().get_tickets(ids)
        return Response(tickets)
