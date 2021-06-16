"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""


from minos.common import Service

from .aggregates import FakePayment


class FakePaymentService(Service):
    """Ticket Service class"""

    @staticmethod
    async def create_fake_payment(
        products: list(int), date: int, state: int
    ) -> FakePayment:
        """
        Creates a fake_payment_service

        :param products: List of `FakePayments`
        :param date: Creation date
        :param state: State of the fake_payment_service
        """
        return await FakePayment.create(products, date, state)

    @staticmethod
    async def get_fake_payments(ids: list[int]) -> list[FakePayment]:
        """Get a list of tickets.

        :param ids: List of ticket identifiers.
        :return: A list of ``Ticket`` instances.
        """
        return await FakePayment.get(ids=ids)
