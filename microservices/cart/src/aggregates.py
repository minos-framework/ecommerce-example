"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import (
    Aggregate,
    AggregateRef,
    ModelRef,
    EntitySet,
    Entity,
)


class Product(AggregateRef):
    """Product AggregateRef class."""

    title: str
    description: str
    price: float


class CartItem(Entity):
    """Cart Item DeclarativeModel class."""

    quantity: int
    product: ModelRef[Product]


class Cart(Aggregate):
    """Cart Aggregate class."""

    user: int
    products: EntitySet[CartItem]
