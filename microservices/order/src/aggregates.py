"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from __future__ import (
    annotations,
)

from datetime import (
    datetime,
)

from minos.common import (
    Aggregate,
    AggregateRef,
    Entity,
    EntitySet,
    ModelRef,
)


class Order(Aggregate):
    """Order Aggregate class."""

    entries: EntitySet[OrderEntry]
    ticket: ModelRef[Ticket]
    status: str

    created_at: datetime
    updated_at: datetime

    user: ModelRef[User]


class OrderEntry(Entity):
    """Order Item class"""

    amount: int
    product: ModelRef[Product]


class Product(AggregateRef):
    """Order AggregateRef class."""

    title: str
    price: float


class Ticket(AggregateRef):
    """Ticket AggregateRef class"""

    total_price: float


class User(AggregateRef):
    """User class"""

    username: str
