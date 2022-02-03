from __future__ import (
    annotations,
)

from minos.aggregate import (
    RootEntity,
    ExternalEntity,
    Ref,
)


class Review(RootEntity):
    """Product Review class."""

    product: Ref[Product]
    user: Ref[Customer]
    title: str
    description: str
    score: int

    @staticmethod
    def validate_score(score: int) -> bool:
        if not isinstance(score, int):
            return False
        return 1 <= score <= 5


class Product(ExternalEntity):
    """Product ExternalEntity class."""

    title: str


class Customer(ExternalEntity):
    """Customer ExternalEntity class."""

    name: str
