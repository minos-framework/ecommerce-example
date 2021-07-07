"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import (
    uuid4,
)

from minos.common import (
    Service,
)
from minos.saga import (
    SagaContext,
)

from .aggregates import (
    Ticket,
)


class TicketService(Service):
    """Ticket Service class"""

    async def create_ticket(self, product_ids: list[int]) -> Ticket:
        """
        Creates a ticket

        :param product_ids: The list of product identifiers to be included in the ticket.
        """
        code = uuid4().hex.upper()[0:6]
        payments = list()
        ticket = await Ticket.create(code, payments, 0.0)
        await self.saga_manager.run("_CreateTicket", context=SagaContext(ticket=ticket, product_ids=product_ids))

        return ticket

    @staticmethod
    async def get_tickets(ids: list[int]) -> list[Ticket]:
        """Get a list of tickets.

        :param ids: List of ticket identifiers.
        :return: A list of ``Ticket`` instances.
        """
        values = {v.id: v async for v in Ticket.get(ids=ids)}
        return [values[id] for id in ids]
