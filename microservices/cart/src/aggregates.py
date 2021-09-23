from __future__ import annotations

from minos.common import (
    Aggregate,
    AggregateRef,
    Entity,
    EntitySet,
    ModelRef,
)


class Cart(Aggregate):
    """Cart Aggregate class."""

    user: int
    entries: EntitySet[CartEntry]


class CartEntry(Entity):
    """Cart Item DeclarativeModel class."""

    quantity: int
    product: ModelRef[Product]


class Product(AggregateRef):
    """Product AggregateRef class."""

    title: str
    description: str
    price: float
