"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.cqrs import (
    CommandService,
)
from minos.networks import (
    Request,
    Response,
    ResponseException,
    enroute,
)
from minos.saga import (
    SagaContext,
    SagaStatus,
)

from .sagas import (
    _CREATE_TICKET,
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
        cart_uuid = content["cart_uuid"]

        saga = await self.saga_manager.run(_CREATE_TICKET, context=SagaContext(cart_uuid=cart_uuid))

        if saga.status == SagaStatus.Finished:
            return Response(saga.context["ticket"])
        else:
            raise ResponseException("An error occurred during order creation.")
