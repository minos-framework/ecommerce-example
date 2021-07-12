"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import UUID

from minos.common import (
    Model,
    ModelType,
)
from minos.saga import (
    Saga,
    SagaContext,
)

_ProductsQuery = ModelType.build("ProductsQuery", {"uuids": list[UUID]})


def _get_products_callback(context: SagaContext) -> Model:
    product_uuids = context["product_uuids"]
    model = _ProductsQuery(uuids=product_uuids)
    return model


def _get_products_reply_callback(products) -> float:
    return sum(product.price for product in products)


async def _commit_callback(context: SagaContext) -> SagaContext:
    ticket = context["ticket"]
    ticket.total_price = context["total_price"]
    await ticket.save()
    return SagaContext(ticket=ticket)


_CREATE_TICKET = (
    Saga("_CreateTicket")
    .step()
    .invoke_participant("GetProducts", _get_products_callback)
    .on_reply("total_price", _get_products_reply_callback)
    .commit(_commit_callback)
)
