"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import (
    UUID,
)

from minos.microservice import (
    Service,
)
from minos.saga import (
    SagaContext,
)

from .aggregates import (
    Shipment,
)


class ShipmentService(Service):
    """Ticket Service class"""

    async def create_shipment(self, products_query) -> UUID:
        """Create a ticket.

        :param products_query: TODO
        :return: The ``UUID`` that identifies the saga execution.
        """
        return await self.saga_manager.run("CreateShipment", context=SagaContext(products_query=products_query))

    @staticmethod
    async def get_shipments(ids: list[int]) -> list[Shipment]:
        """Get a list of tickets.

        :param ids: List of ticket identifiers.
        :return: A list of ``Ticket`` instances.
        """
        return await Shipment.get(ids=ids)
