from __future__ import (
    annotations,
)

from minos.aggregate import (
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
