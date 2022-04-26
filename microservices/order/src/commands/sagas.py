from collections import (
    defaultdict,
)
from uuid import (
    UUID,
)

from minos.common import (
    Inject,
    ModelType,
)
from minos.saga import (
    Saga,
    SagaContext,
    SagaRequest,
    SagaResponse,
)

from ..aggregates import (
    Order,
    OrderAggregate,
    OrderStatus,
)

PurchaseProductsQuery = ModelType.build("PurchaseProductsQuery", {"quantities": dict[str, int]})
TicketQuery = ModelType.build("TicketQuery", {"cart_uuid": UUID})
PaymentQuery = ModelType.build("PaymentQuery", {"credit_number": int, "amount": float})


def _create_ticket(context: SagaContext) -> SagaRequest:
    cart_uuid = context["cart_uuid"]
    return SagaRequest("CreateTicket", TicketQuery(cart_uuid))


async def _process_ticket_entries(context: SagaContext, response: SagaResponse) -> SagaContext:
    ticket = await response.content()
    product_uuids = list()
    for entry in ticket.entries.data.values():
        product_uuids.append(str(entry.product))
    context["ticket"] = dict(uuid=ticket.uuid, product_uuids=product_uuids, total_amount=ticket.total_price)
    return context


def _purchase_products(context: SagaContext) -> SagaRequest:
    product_uuids = context["ticket"]["product_uuids"]
    quantities = defaultdict(int)
    for product_uuid in product_uuids:
        quantities[str(product_uuid)] += 1

    return SagaRequest("PurchaseProducts", PurchaseProductsQuery(quantities))


# noinspection PyUnusedLocal
def _raise(context: SagaContext, response: SagaResponse) -> SagaContext:
    raise ValueError("Errored response must abort the execution!")


def _revert_purchase_products(context: SagaContext) -> SagaRequest:
    product_uuids = context["ticket"]["product_uuids"]
    quantities = defaultdict(int)
    for product_uuid in product_uuids:
        quantities[str(product_uuid)] -= 1

    return SagaRequest("PurchaseProducts", PurchaseProductsQuery(quantities))


def _payment(context: SagaContext) -> SagaRequest:
    amount = context["ticket"]["total_amount"]
    card_number = context["payment_detail"].card_number
    return SagaRequest("CreatePayment", PaymentQuery(card_number, amount))


async def _get_payment(context: SagaContext, response: SagaResponse) -> SagaContext:
    value = await response.content()
    context["payment"] = value.uuid
    return context


@Inject()
async def _create_commit_callback(context: SagaContext, aggregate: OrderAggregate) -> SagaContext:
    order = await Order.create(
        ticket=context["ticket"]["uuid"],
        payment=context["payment"],
        payment_detail=context["payment_detail"],
        shipment_detail=context["shipment_detail"],
        total_amount=context["ticket"]["total_amount"],
        status=OrderStatus.COMPLETED,
        customer=context["customer_uuid"],
    )

    return SagaContext(order=order)


CREATE_ORDER = (
    Saga()
    .remote_step(_create_ticket)
    .on_success(_process_ticket_entries)
    .remote_step(_purchase_products)
    .on_error(_raise)
    .on_failure(_revert_purchase_products)
    .remote_step(_payment)
    .on_success(_get_payment)
    .commit(_create_commit_callback)
)
