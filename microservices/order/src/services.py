"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import UUID

from minos.common import Service
from minos.saga import SagaContext

from .aggregates import Order


class OrderService(Service):
    """Ticket Service class"""

    async def create_order(self, products: list[int]) -> UUID:
        """
        Creates a fake_payment_service

        :param products: List of `orders`
        """
        return await self.saga_manager.run("CreateOrder", context=SagaContext(product_ids=products))

    @staticmethod
    async def get_orders(ids: list[int]) -> list[Order]:
        """Get a list of tickets.

        :param ids: List of ticket identifiers.
        :return: A list of ``Ticket`` instances.
        """
        values = {v.id: v async for v in Order.get(ids=ids)}
        return [values[id] for id in ids]
