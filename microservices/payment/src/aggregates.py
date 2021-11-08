from minos.aggregate import (
    Aggregate,
)


class Payment(Aggregate):
    """Payment Aggregate class."""

    credit_number: int
    amount: float
    status: str
