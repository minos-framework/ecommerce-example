from __future__ import annotations

from minos.aggregate import (
    RootEntity,
    ExternalEntity,
    Entity,
    EntitySet,
    Ref,
)


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
