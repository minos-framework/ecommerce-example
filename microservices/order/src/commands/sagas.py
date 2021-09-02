"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from collections import defaultdict
from uuid import UUID

from minos.common import (
    Aggregate,
    Model,
    ModelType,
)
from minos.saga import (
    Saga,
    SagaContext,
)

from ..aggregates import Order

PurchaseProductsQuery = ModelType.build("PurchaseProductsQuery", {"quantities": dict[str, int]})
ProductsQuery = ModelType.build("ProductsQuery", {"product_uuids": list[UUID]})


def _purchase_products(context: SagaContext) -> Model:
    product_uuids = context["product_uuids"]
    quantities = defaultdict(int)
    for product_uuid in product_uuids:
        quantities[str(product_uuid)] += 1

    return PurchaseProductsQuery(quantities)


def _revert_purchase_products(context: SagaContext) -> Model:
    product_uuids = context["product_uuids"]
    quantities = defaultdict(int)
    for product_uuid in product_uuids:
        quantities[str(product_uuid)] -= 1

    return PurchaseProductsQuery(quantities)


def _create_ticket(context: SagaContext) -> Model:
    product_uuids = context["product_uuids"]
    model = ProductsQuery(product_uuids)
    return model


def _create_ticket_reply(value: Aggregate) -> UUID:
    return value.uuid


async def _create_commit_callback(context: SagaContext) -> SagaContext:
    product_uuids = context["product_uuids"]
    ticket_uuid = context["ticket_uuid"]
    status = "created"
    order = await Order.create(product_uuids, ticket_uuid, status)
    return SagaContext(order=order)


CREATE_ORDER = (
    Saga()
    .step()
    .invoke_participant("PurchaseProducts", _purchase_products)
    .with_compensation("PurchaseProducts", _revert_purchase_products)
    .step()
    .invoke_participant("CreateTicket", _create_ticket)
    .on_reply("ticket_uuid", _create_ticket_reply)
    .commit(_create_commit_callback)
)
