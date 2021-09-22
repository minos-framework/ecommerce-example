from __future__ import (
    annotations,
)

from minos.common import (
    Aggregate,
    AggregateRef,
    ModelRef,
)


class Review(Aggregate):
    """Product Review class."""

    product: ModelRef[Product]
    user: ModelRef[Customer]
    title: str
    description: str
    score: int

    @staticmethod
    def validate_score(score: int) -> bool:
        if not isinstance(score, int):
            return False
        return 1 <= score <= 5


class Product(AggregateRef):
    """Product AggregateRef class."""

    title: str


class Customer(AggregateRef):
    """Customer AggregateRef class."""

    username: str
