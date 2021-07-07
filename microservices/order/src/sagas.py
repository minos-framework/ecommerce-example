"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from collections import defaultdict
from datetime import datetime

from minos.common import (
    Model,
    ModelType,
)
from minos.saga import (
    Saga,
    SagaContext,
)

from .aggregates import Order

_ReserveProductsQuery = ModelType.build("ValidateProductsQuery", {"quantities": dict[str, int]})


def _reserve_products_callback(context: SagaContext) -> Model:
    product_ids = context["product_ids"]
    quantities = defaultdict(int)
    for product_id in product_ids:
        quantities[str(product_id)] += 1

    return _ReserveProductsQuery(quantities=quantities)


def _release_products_callback(context: SagaContext) -> Model:
    product_ids = context["product_ids"]
    quantities = defaultdict(int)
    for product_id in product_ids:
        quantities[str(product_id)] -= 1

    return _ReserveProductsQuery(quantities=quantities)


def _create_ticket_callback(context: SagaContext) -> Model:
    product_ids = context["product_ids"]
    _ProductsQ = ModelType.build("ProductsQuery", {"product_ids": list[int]})
    model = _ProductsQ(product_ids=product_ids)
    return model


def _create_ticket_reply_callback(value) -> int:
    return value.id


async def _create_commit_callback(context: SagaContext) -> SagaContext:
    product_ids = context["product_ids"]
    ticket_id = context["ticket_id"]
    now = datetime.now()
    status = "created"
    order = await Order.create(product_ids, ticket_id, status, created_at=now, updated_at=now)
    return SagaContext(order=order)


CREATE_ORDER = (
    Saga("CreateOrder")
    .step()
    .invoke_participant("ReserveProducts", _reserve_products_callback)
    .with_compensation("ReserveProducts", _release_products_callback)
    .step()
    .invoke_participant("CreateTicket", _create_ticket_callback)
    .on_reply("ticket_id", _create_ticket_reply_callback)
    .commit(_create_commit_callback)
)
