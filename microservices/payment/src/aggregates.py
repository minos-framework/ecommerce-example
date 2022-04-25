from typing import (
    Optional,
)

from minos.aggregate import (
    Aggregate,
    RootEntity,
)


class Payment(RootEntity):
    """Payment RootEntity class."""

    credit_number: int
    amount: float
    status: str


class PaymentAggregate(Aggregate[Payment]):
    """Payment Aggregate class."""

    @staticmethod
    async def create_payment(credit_number: int, amount: float, status: Optional[str] = None) -> Payment:
        """TODO"""
        if status is None:
            status = "created"
        payment = await Payment.create(credit_number, amount, status)
        return payment
