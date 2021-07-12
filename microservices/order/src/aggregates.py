"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from datetime import (
    datetime,
)

from minos.common import (
    Aggregate,
    ModelRef,
    SubAggregate,
)


class Product(SubAggregate):
    """Order SubAggregate class."""


class Ticket(SubAggregate):
    """Ticket SubAggregate class"""


class Order(Aggregate):
    """Order Aggregate class."""

    products: list[ModelRef[Product]]
    ticket: ModelRef[Ticket]
    status: str

    created_at: datetime
    updated_at: datetime
