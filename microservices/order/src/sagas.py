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
from uuid import UUID

from minos.common import (
    Aggregate, Model,
    ModelType,
)
from minos.saga import (
    Saga,
    SagaContext,
)

from .aggregates import (
    Order,
)

_ReserveProductsQuery = ModelType.build("ValidateProductsQuery", {"quantities": dict[str, int]})


def _reserve_products_callback(context: SagaContext) -> Model:
    product_uuids = context["product_uuids"]
    quantities = defaultdict(int)
    for product_uuid in product_uuids:
        quantities[str(product_uuid)] += 1

    return _ReserveProductsQuery(quantities=quantities)


def _release_products_callback(context: SagaContext) -> Model:
    product_uuids = context["product_uuids"]
    quantities = defaultdict(int)
    for product_uuid in product_uuids:
        quantities[str(product_uuid)] -= 1

    return _ReserveProductsQuery(quantities=quantities)


def _create_ticket_callback(context: SagaContext) -> Model:
    product_uuids = context["product_uuids"]
    _ProductsQ = ModelType.build("ProductsQuery", {"product_uuids": list[UUID]})
    model = _ProductsQ(product_uuids=product_uuids)
    return model


def _create_ticket_reply_callback(value: Aggregate) -> UUID:
    return value.uuid


async def _create_commit_callback(context: SagaContext) -> SagaContext:
    product_uuids = context["product_uuids"]
    ticket_uuid = context["ticket_uuid"]
    now = datetime.now()
    status = "created"
    order = await Order.create(product_uuids, ticket_uuid, status, created_at=now, updated_at=now)
    return SagaContext(order=order)


CREATE_ORDER = (
    Saga("CreateOrder")
    .step()
    .invoke_participant("ReserveProducts", _reserve_products_callback)
    .with_compensation("ReserveProducts", _release_products_callback)
    .step()
    .invoke_participant("CreateTicket", _create_ticket_callback)
    .on_reply("ticket_uuid", _create_ticket_reply_callback)
    .commit(_create_commit_callback)
)
