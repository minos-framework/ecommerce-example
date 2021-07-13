"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import (
    UUID,
)

from minos.common import (
    Service,
)

from ..aggregates import (
    Payment,
)


class PaymentCommandService(Service):
    """Ticket Service class"""

    @staticmethod
    async def create_payment(credit_number: int, amount: float) -> Payment:
        """
        Creates a payment

        :param credit_number: TODO
        :param amount; TODO
        """
        status = "created"
        return await Payment.create(credit_number, amount, status)

    @staticmethod
    async def get_payments(uuids: list[UUID]) -> list[Payment]:
        """Get a list of tickets.

        :param uuids: List of ticket identifiers.
        :return: A list of ``Ticket`` instances.
        """
        values = {v.uuid: v async for v in Payment.get(uuids=uuids)}
        return [values[uuid] for uuid in uuids]
