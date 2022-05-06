from __future__ import (
    annotations,
)

from uuid import (
    UUID,
    uuid4,
)

from minos.aggregate import (
    Aggregate,
    Entity,
    EntitySet,
    Ref,
)
from minos.common import (
    Inject,
)
from minos.saga import (
    SagaContext,
    SagaManager,
    SagaStatus,
)


class Ticket(Entity):
    """Ticket Entity class."""

    code: str
    total_price: float
    entries: EntitySet[Ref[TicketEntry]]


# noinspection PyUnresolvedReferences
class TicketEntry(Entity):
    """TicketEntry Entity class."""

    title: str
    unit_price: float
    quantity: int
    product: Ref["src.aggregates.Product"]


# noinspection PyUnresolvedReferences
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

    async def create_ticket_instance(self, total_price: float, entries: EntitySet[TicketEntry]) -> Ticket:
        """TODO"""
        ticket, delta = await self.repository.create(
            Ticket, code=uuid4().hex.upper()[0:6], total_price=total_price, entries=entries,
        )
        await self.publish_domain_event(delta)
        return ticket

    async def create_ticket_entry_instance(
        self, title: str, unit_price: float, quantity: int, product: Ref["src.aggregates.Product"]
    ) -> TicketEntry:
        """TODO"""
        entry, delta = await self.repository.create(
            TicketEntry, title=title, unit_price=unit_price, quantity=quantity, product=product
        )
        await self.publish_domain_event(delta)
        return entry
