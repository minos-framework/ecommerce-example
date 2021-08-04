"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import (
    uuid4,
)

from minos.cqrs import (
    CommandService,
)
from minos.networks import (
    Request,
    Response,
    enroute,
)
from minos.saga import (
    SagaContext,
)

from ..aggregates import (
    Ticket,
)


class TicketCommandService(CommandService):
    """Ticket Service class"""

    @enroute.rest.command("/tickets", "POST")
    @enroute.broker.command("CreateTicket")
    async def create_ticket(self, request: Request) -> Response:
        """Create a new ticket.

        :param request: The ``Request`` instance to be use to compute the price.
        :return: A ``Response`` containing the created ticket.
        """
        content = await request.content()
        product_uuids = content["product_uuids"]
        code = uuid4().hex.upper()[0:6]
        payments = list()
        ticket = await Ticket.create(code, payments, 0.0)
        await self.saga_manager.run("_CreateTicket", context=SagaContext(ticket=ticket, product_uuids=product_uuids))

        return Response(ticket)
