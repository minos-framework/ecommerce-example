"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import (
    UUID,
    uuid4,
)

from minos.common import (
    ModelType,
    Request,
    Response,
    Service,
)
from minos.saga import SagaContext

from ..aggregates import Ticket


class TicketCommandService(Service):
    """Ticket Service class"""

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

    @staticmethod
    async def get_tickets(request: Request) -> Response:
        """Get a list of tickets by uuid.

        :param request: A ``Request`` instance containing the list of ticket identifiers.
        :return: A ``Response`` containing the list of requested tickets.
        """
        _Query = ModelType.build("Query", {"uuids": list[UUID]})
        content = await request.content(model_type=_Query)
        uuids = content["uuids"]

        values = {v.uuid: v async for v in Ticket.get(uuids=uuids)}
        tickets = [values[uuid] for uuid in uuids]

        return Response(tickets)
