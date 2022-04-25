from minos.aggregate import (
    RootEntity,
)
from minos.aggregate import Aggregate


class Payment(RootEntity):
    """Payment RootEntity class."""

    credit_number: int
    amount: float
    status: str


class PaymentAggregate(Aggregate[Payment]):
    """Payment Aggregate class."""
