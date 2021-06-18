"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import Service

from .aggregates import Product


class OrderService(Service):
    """Ticket Service class"""
    @staticmethod
    async def create_order(orders: list(int), date: int,
                           state: int) -> Product:
        """
        Creates a fake_payment_service

        :param products: List of `Products`
        :param date: Creation date
        :param state: State of the fake_payment_service
        """
        return await Order.create(products, date, state)

    @staticmethod
    async def get_orders(ids: list[int]) -> list[Order]:
        """Get a list of tickets.

        :param ids: List of ticket identifiers.
        :return: A list of ``Ticket`` instances.
        """
        return await Order.get(ids=ids)