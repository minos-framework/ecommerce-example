"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from __future__ import annotations

from minos.common import (
    Aggregate,
    AggregateRef,
    Entity,
    EntitySet,
    ModelRef,
)


class Ticket(Aggregate):
    """Ticket Aggregate class."""

    code: str
    total_price: float
    entries: EntitySet[TicketEntry]


class TicketEntry(Entity):
    """Order Item class"""

    title: str
    unit_price: float
    quantity: int
    product: ModelRef[Product]


class Product(AggregateRef):
    """Order AggregateRef class."""

    title: str
    price: float
