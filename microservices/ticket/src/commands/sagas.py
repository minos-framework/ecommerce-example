"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import (
    UUID, uuid4,
)

from minos.common import (
    Model,
    ModelType, EntitySet,
)
from minos.saga import (
    Saga,
    SagaContext,
)

from src import TicketEntry, Ticket

CartQuery = ModelType.build("CartQuery", {"uuid": UUID})


def _get_cart_items(context: SagaContext) -> Model:
    cart_uuid = context["cart_uuid"]
    return CartQuery(cart_uuid)


async def _process_cart_items(cart) -> dict:
    cart_products = cart["products"]

    ticket_entries = EntitySet()
    product_uuids = list()
    total_amount = 0
    for product in cart_products:
        total_price = product.price * product.quantity
        total_amount += total_price
        order_entry = TicketEntry(
            title=product.title, unit_price=product.price, quantity=product.quantity, product=product.product_id
        )
        ticket_entries.add(order_entry)

        product_uuids.append(str(product.product_id))

    return dict(ticket_entries=ticket_entries, total_amount=total_amount, product_uuids=product_uuids)


async def _commit_callback(context: SagaContext) -> SagaContext:
    ticket = await Ticket.create(
        code=uuid4().hex.upper()[0:6],
        total_price=context["products"]["total_amount"],
        entries=context["products"]["ticket_entries"]
    )

    return SagaContext(ticket=ticket)


_CREATE_TICKET = (
    Saga("_CreateTicket")
    .step()
    .invoke_participant("GetCart", _get_cart_items)
    .on_reply("products", _process_cart_items)
    .commit(_commit_callback)
)
