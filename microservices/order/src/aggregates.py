"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from __future__ import annotations

from datetime import datetime

from minos.common import (
    Aggregate,
    AggregateRef,
    ModelRef,
)


class Order(Aggregate):
    """Order Aggregate class."""

    products: list[ModelRef[Product]]
    ticket: ModelRef[Ticket]
    status: str

    created_at: datetime
    updated_at: datetime


class Product(AggregateRef):
    """Order AggregateRef class."""

    price: float


class Ticket(AggregateRef):
    """Ticket AggregateRef class"""
