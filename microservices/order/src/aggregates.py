"""src.aggregates module."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from minos.common import (
    Aggregate,
    AggregateRef,
    Entity,
    EntitySet,
    ModelRef,
    ValueObject,
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
    total_amount: Optional[float]

    created_at: datetime
    updated_at: datetime

    customer: ModelRef[Customer]


class Ticket(AggregateRef):
    """Ticket Aggregate class."""

    total_price: float
    entries: EntitySet[TicketEntry]


class TicketEntry(Entity):
    """Order Item class"""

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


class Customer(AggregateRef):
    """User class"""

    name: str
    surname: str
