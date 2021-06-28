"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from collections import defaultdict
from datetime import (
    datetime,
)

from minos.common import (
    Model,
    ModelType,
)
from minos.saga import (
    Saga,
    SagaContext,
)

from .aggregates import (
    Order,
)

_ProductsQuery = ModelType.build("ProductsQuery", {"ids": list[int]})
_ValidateProductsQuery = ModelType.build("ValidateProductsQuery", {"quantities": dict[str, int]})


def _validate_products_callback(context: SagaContext) -> Model:
    product_ids = context["product_ids"]
    model = _ProductsQuery(ids=product_ids)
    return model


def _validate_products_reply_callback(value) -> None:
    if not value.exist:
        raise ValueError("One or more products do not exist.")


def _reserve_products_callback(context: SagaContext) -> Model:
    product_ids = context["product_ids"]
    quantities = defaultdict(int)
    for product_id in product_ids:
        quantities[str(product_id)] += 1

    model = _ValidateProductsQuery(quantities=quantities)
    return model


def _release_products_callback(context: SagaContext) -> Model:
    product_ids = context["product_ids"]
    quantities = defaultdict(int)
    for product_id in product_ids:
        quantities[str(product_id)] -= 1

    model = _ValidateProductsQuery(quantities=quantities)
    return model


def _reserve_products_reply_callback(value) -> None:
    if not value.exist:
        raise ValueError("One or more products have not enough stock.")


async def _create_commit_callback(context: SagaContext) -> SagaContext:
    product_ids = context["product_ids"]
    now = datetime.now()
    status = "created"
    order = await Order.create(product_ids, status, created_at=now, updated_at=now)
    return SagaContext(order=order)


CREATE_ORDER = (
    Saga("CreateOrder")
    .step()
    .invoke_participant("ValidateProducts", _validate_products_callback)
    .on_reply("_", _validate_products_reply_callback)
    .step()
    .invoke_participant("ReserveProducts", _reserve_products_callback)
    .with_compensation("ReserveProducts", _release_products_callback)
    .on_reply("_", _reserve_products_reply_callback)
    .commit(_create_commit_callback)
)
