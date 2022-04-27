from __future__ import (
    annotations,
)

from asyncio import gather
from datetime import (
    datetime,
)
from enum import (
    Enum,
)
from typing import (
    Any,
    Optional,
)
from uuid import (
    UUID,
)

from minos.aggregate import (
    Aggregate,
    Entity,
    EntitySet,
    ExternalEntity,
    Ref,
    RootEntity,
    ValueObject, Action, IncrementalFieldDiff, Event,
)
from minos.common import (
    Inject,
)
from minos.networks import (
    BrokerMessageV1,
    BrokerMessageV1Payload,
)
from minos.saga import (
    SagaContext,
    SagaManager,
    SagaStatus,
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

    @Inject()
    def __init__(self, *args, saga_manager: SagaManager, **kwargs):
        super().__init__(*args, **kwargs)
        self.saga_manager = saga_manager

    async def create_order(
        self, cart_uuid: UUID, customer_uuid: UUID, payment: dict[str, Any], shipment: dict[str, Any]
    ) -> Order:
        """TODO"""
        from .commands import (
            CREATE_ORDER,
        )

        payment_detail = PaymentDetail(**payment)
        shipment_detail = ShipmentDetail(**shipment)

        execution = await self.saga_manager.run(
            CREATE_ORDER,
            context=SagaContext(
                cart_uuid=cart_uuid,
                customer_uuid=customer_uuid,
                payment_detail=payment_detail,
                shipment_detail=shipment_detail,
            ),
            raise_on_error=False,
        )

        if execution.status != SagaStatus.Finished:
            raise ValueError("An error occurred during order creation.")

        return execution.context["order"]

    async def create_order_instance(
        self,
        ticket: Ref[Ticket],
        payment: Ref[Payment],
        payment_detail: PaymentDetail,
        shipment_detail: ShipmentDetail,
        total_amount: float,
        customer: Ref[Customer],
    ) -> Order:
        """TODO"""
        order, delta = await self.repository.create(
            Order,
            ticket=ticket,
            payment=payment,
            payment_detail=payment_detail,
            shipment_detail=shipment_detail,
            total_amount=total_amount,
            status=OrderStatus.COMPLETED,
            customer=customer,
        )
        await self.publish_domain_event(delta)

        return order