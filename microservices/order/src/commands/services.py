"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import UUID

from minos.common import Service
from minos.saga import SagaContext

from ..aggregates import Order


class OrderCommandService(Service):
    """Ticket Service class"""

    async def create_order(self, product_uuids: list[UUID]) -> UUID:
        """
        Creates a fake_payment_service

        :param product_uuids: List of `orders`
        """
        return await self.saga_manager.run("CreateOrder", context=SagaContext(product_uuids=product_uuids))

    @staticmethod
    async def get_orders(uuids: list[UUID]) -> list[Order]:
        """Get a list of tickets.

        :param uuids: List of ticket identifiers.
        :return: A list of ``Ticket`` instances.
        """
        values = {v.uuid: v async for v in Order.get(uuids=uuids)}
        return [values[uuid] for uuid in uuids]
