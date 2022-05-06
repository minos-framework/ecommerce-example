from typing import (
    Optional,
)

from minos.aggregate import (
    Aggregate,
    Entity,
)


class Payment(Entity):
    """Payment Entity class."""

    credit_number: int
    amount: float
    status: str


class PaymentAggregate(Aggregate[Payment]):
    """Payment Aggregate class."""

    async def create_payment(self, credit_number: int, amount: float, status: Optional[str] = None) -> Payment:
        """TODO"""
        if status is None:
            status = "created"

        payment, delta = await self.repository.create(Payment, credit_number, amount, status)
        await self.publish_domain_event(delta)

        return payment
