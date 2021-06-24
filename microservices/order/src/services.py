"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from datetime import (
    datetime,
)

from minos.common import (
    Service,
)

from .aggregates import (
    Order,
)


class OrderService(Service):
    """Ticket Service class"""

    @staticmethod
    async def create_order(products: list[int]) -> Order:
        """
        Creates a fake_payment_service

        :param products: List of `orders`
        """
        now = datetime.now()
        status = "created"
        return await Order.create(products, status, created_at=now, updated_at=now)

    @staticmethod
    async def get_orders(ids: list[int]) -> list[Order]:
        """Get a list of tickets.

        :param ids: List of ticket identifiers.
        :return: A list of ``Ticket`` instances.
        """
        values = {v.id: v async for v in Order.get(ids=ids)}
        return [values[id] for id in ids]
