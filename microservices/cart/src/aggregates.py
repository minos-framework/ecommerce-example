"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from __future__ import (
    annotations,
)

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
