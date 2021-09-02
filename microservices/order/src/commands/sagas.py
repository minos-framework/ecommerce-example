"""
Copyright (C) 2021 Clariteia SL
This file is part of minos framework.
Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from collections import (
    defaultdict,
)
from datetime import (
    datetime,
)
from uuid import (
    UUID,
)

from minos.common import (
    Aggregate,
    EntitySet,
    Model,
    ModelType,
)
from minos.saga import (
    Saga,
    SagaContext,
)

from ..aggregates import (
    Order,
    OrderStatus,
)

PurchaseProductsQuery = ModelType.build("PurchaseProductsQuery", {"quantities": dict[str, int]})
TicketQuery = ModelType.build("TicketQuery", {"cart_uuid": UUID})
PaymentQuery = ModelType.build("PaymentQuery", {"credit_number": int, "amount": float})


def _create_ticket(context: SagaContext) -> Model:
    cart_uuid = context["cart_uuid"]
    return TicketQuery(cart_uuid)


async def _process_ticket_entries(ticket) -> dict:
    product_uuids = list()
    for entry in ticket.entries.data.values():
        product_uuids.append(str(entry.product))
    return dict(uuid=ticket.uuid, product_uuids=product_uuids, total_amount=ticket.total_price)


def _purchase_products(context: SagaContext) -> Model:
    product_uuids = context["ticket"]["product_uuids"]
    quantities = defaultdict(int)
    for product_uuid in product_uuids:
        quantities[str(product_uuid)] += 1

    return PurchaseProductsQuery(quantities)


def _revert_purchase_products(context: SagaContext) -> Model:
    product_uuids = context["ticket"]["product_uuids"]
    quantities = defaultdict(int)
    for product_uuid in product_uuids:
        quantities[str(product_uuid)] -= 1

    return PurchaseProductsQuery(quantities)


def _payment(context: SagaContext) -> Model:
    amount = context["ticket"]["total_amount"]
    card_number = context["payment_detail"].card_number
    return PaymentQuery(card_number, amount)


def _get_payment(value: Aggregate) -> UUID:
    return value.uuid


async def _create_commit_callback(context: SagaContext) -> SagaContext:
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
    Saga("CreateOrder")
    .step()
    .invoke_participant("CreateTicket", _create_ticket)
    .on_reply("ticket", _process_ticket_entries)
    .step()
    .invoke_participant("PurchaseProducts", _purchase_products)
    .with_compensation("PurchaseProducts", _revert_purchase_products)
    .step()
    .invoke_participant("CreatePayment", _payment)
    .on_reply("payment", _get_payment)
    .commit(_create_commit_callback)
)
