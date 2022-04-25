from __future__ import (
    annotations,
)

from minos.aggregate import (
    Entity,
    EntitySet,
    ExternalEntity,
    Ref,
    RootEntity,
)
from minos.aggregate import Aggregate


class Cart(RootEntity):
    """Cart RootEntity class."""

    user: int
    entries: EntitySet[CartEntry]


class CartEntry(Entity):
    """Cart Item DeclarativeModel class."""

    quantity: int
    product: Ref[Product]


class Product(ExternalEntity):
    """Product ExternalEntity class."""

    title: str
    description: str
    price: float


class CartAggregate(Aggregate[Cart]):
    """Cart Aggregate class."""
