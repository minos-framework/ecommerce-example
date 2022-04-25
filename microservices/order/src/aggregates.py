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

from minos.aggregate import (
    Aggregate,
    Entity,
    EntitySet,
    ExternalEntity,
    Ref,
    RootEntity,
    ValueObject,
)
from minos.networks import (
    BrokerMessageV1,
    BrokerMessageV1Payload,
)


class OrderStatus(str, Enum):
    CREATED = "created"
    PROCESSING = "processing"
    COMPLETED = "completed"


class Order(RootEntity):
    """Order RootEntity class."""

    ticket: Optional[Ref[Ticket]]

    payment: Optional[Ref[Payment]]
    payment_detail: PaymentDetail

    # TODO: Future Shipment Microservice
    shipment_detail: ShipmentDetail

    status: OrderStatus
    total_amount: Optional[float]

    created_at: datetime
    updated_at: datetime

    customer: Ref[Customer]


class Ticket(ExternalEntity):
    """Ticket RootEntity class."""

    total_price: float
    entries: EntitySet[TicketEntry]


class TicketEntry(Entity):
    """Order Item class"""

    quantity: int
    product: Ref[Product]


class Product(ExternalEntity):
    """Order ExternalEntity class."""

    title: str
    price: float


class PaymentDetail(ValueObject):
    card_holder: str
    card_number: int
    card_expire: str
    card_cvc: str


class Payment(ExternalEntity):
    """Payment ExternalEntity class"""

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


class Customer(ExternalEntity):
    """User class"""

    name: str
    surname: str


class OrderAggregate(Aggregate[Order]):
    """Order Aggregate class."""

    async def something(self):
        message = BrokerMessageV1("foo", BrokerMessageV1Payload("bar"),)
        await self.broker_publisher.send(message)
