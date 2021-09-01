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
from enum import (
    Enum,
)
from typing import (
    Optional,
)

from minos.common import (
    Aggregate,
    AggregateRef,
    ModelRef,
    ValueObject,
    Entity,
    EntitySet,
)


class OrderStatus(str, Enum):
    CREATED = "created"
    PROCESSING = "processing"
    COMPLETED = "completed"


class Order(Aggregate):
    """Order Aggregate class."""

    ticket: Optional[ModelRef[Ticket]]

    payment: Optional[ModelRef[Payment]]
    payment_detail: PaymentDetail

    # TODO: Future Shipment Microservice
    shipment_detail: ShipmentDetail

    status: OrderStatus

    created_at: datetime
    updated_at: datetime

    user: ModelRef[User]


class Ticket(Aggregate):
    """Ticket Aggregate class."""
    code: Optional[str]
    total_price: Optional[float]
    entries: Optional[EntitySet[TicketEntry]]


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


class PaymentDetail(ValueObject):
    card_holder: str
    card_number: int
    card_expire: str
    card_cvc: str


class Payment(AggregateRef):
    """Payment AggregateRef class"""

    status: str


class ShipmentDetail(ValueObject):
    name: str
    last_name: str
    email: str
    address: str
    country: str
    city: str
    province: str
    zip: int


class User(AggregateRef):
    """User class"""

    username: str


