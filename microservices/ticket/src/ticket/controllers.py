"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import Request
from minos.common import Response

from .dto import TicketDto
from .dto import TicketsQueryDto
from .services import TicketService


class TicketController:
    """Ticket Controller class"""

    @staticmethod
    async def create_ticket(request: Request) -> Response:
        """TODO

        :param request:TODO
        :return: TODO
        """
        content = await request.content()
        ticket = await TicketService().create_ticket(**content[0])
        return Response(ticket)

    @staticmethod
    async def get_tickets(request: Request) -> Response:
        """TODO

        :param request: TODO
        :return: TODO
        """
        content = await request.content()
        if len(content) and isinstance(content[0], TicketsQueryDto):
            content = content[0].ids
        tickets = [
            TicketDto.from_dict(ticket.avro_data)
            for ticket in await TicketService().get_tickets(content)
        ]
        return Response(tickets)
