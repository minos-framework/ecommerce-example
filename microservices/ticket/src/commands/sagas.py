from uuid import (
    UUID,
    uuid4,
)

from minos.aggregate import EntitySet
from minos.common import ModelType
from minos.saga import (
    Saga,
    SagaContext,
    SagaRequest,
    SagaResponse,
)

from src import (
    Ticket,
    TicketEntry,
)

CartQuery = ModelType.build("CartQuery", {"uuid": UUID})


def _get_cart_items(context: SagaContext) -> SagaRequest:
    cart_uuid = context["cart_uuid"]
    return SagaRequest("GetCartQRS", CartQuery(cart_uuid))


async def _process_cart_items(context: SagaContext, response: SagaResponse) -> SagaContext:
    cart = await response.content()

    cart_products = cart["products"]

    ticket_entries = EntitySet()
    total_amount = 0
    for product in cart_products:
        total_price = product.price * product.quantity
        total_amount += total_price
        order_entry = TicketEntry(
            title=product.title, unit_price=product.price, quantity=product.quantity, product=product.product_id
        )
        ticket_entries.add(order_entry)

    context["products"] = dict(ticket_entries=ticket_entries, total_amount=total_amount)
    return context


async def _commit_callback(context: SagaContext) -> SagaContext:
    ticket = await Ticket.create(
        code=uuid4().hex.upper()[0:6],
        total_price=context["products"]["total_amount"],
        entries=context["products"]["ticket_entries"],
    )

    return SagaContext(ticket=ticket)


_CREATE_TICKET = Saga().remote_step(_get_cart_items).on_success(_process_cart_items).commit(_commit_callback)
