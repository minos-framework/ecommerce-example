"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import (
    Service,
)

from .aggregates import (
    Payment,
)


class PaymentService(Service):
    """Ticket Service class"""

    @staticmethod
    async def create_payment(products: list[int], date: int, state: int) -> Payment:
        """
        Creates a payment_service

        :param products: List of `Payments`
        :param date: Creation date
        :param state: State of the payment_service
        """
        return await Payment.create(products, date, state)

    @staticmethod
    async def get_payments(ids: list[int]) -> list[Payment]:
        """Get a list of tickets.

        :param ids: List of ticket identifiers.
        :return: A list of ``Ticket`` instances.
        """
        values = {v.id: v async for v in Payment.get(ids=ids)}
        return [values[id] for id in ids]
