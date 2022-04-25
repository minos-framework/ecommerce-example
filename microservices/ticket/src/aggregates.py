from __future__ import (
    annotations,
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
)
from minos.common import (
    Inject,
)
from minos.saga import (
    SagaContext,
    SagaManager,
    SagaStatus,
)


class Ticket(RootEntity):
    """Ticket RootEntity class."""

    code: str
    total_price: float
    entries: EntitySet[TicketEntry]


class TicketEntry(Entity):
    """Order Item class"""

    title: str
    unit_price: float
    quantity: int
    product: Ref[Product]


class Product(ExternalEntity):
    """Order ExternalEntity class."""

    title: str
    price: float


class TicketAggregate(Aggregate[Ticket]):
    """Ticket Aggregate class."""

    @Inject()
    def __init__(self, *args, saga_manager: SagaManager, **kwargs):
        super().__init__(*args, **kwargs)
        self.saga_manager = saga_manager

    async def create_ticket(self, cart_uuid: UUID) -> Ticket:
        """TODO"""
        from .commands import (
            _CREATE_TICKET,
        )

        execution = await self.saga_manager.run(
            _CREATE_TICKET, context=SagaContext(cart_uuid=cart_uuid), raise_on_error=False,
        )

        if execution.status != SagaStatus.Finished:
            raise ValueError("An error occurred during order creation.")

        return execution.context["ticket"]
