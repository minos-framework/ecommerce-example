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
    Service,
)
from minos.saga import (
    SagaContext,
)

from ..aggregates import (
    Ticket,
)


class TicketCommandService(Service):
    """Ticket Service class"""

    async def create_ticket(self, product_uuids: list[UUID]) -> Ticket:
        """
        Creates a ticket

        :param product_uuids: The list of product identifiers to be included in the ticket.
        """
        code = uuid4().hex.upper()[0:6]
        payments = list()
        ticket = await Ticket.create(code, payments, 0.0)
        await self.saga_manager.run("_CreateTicket", context=SagaContext(ticket=ticket, product_uuids=product_uuids))

        return ticket

    @staticmethod
    async def get_tickets(uuids: list[UUID]) -> list[Ticket]:
        """Get a list of tickets.

        :param uuids: List of ticket identifiers.
        :return: A list of ``Ticket`` instances.
        """
        values = {v.uuid: v async for v in Ticket.get(uuids=uuids)}
        return [values[uuid] for uuid in uuids]
