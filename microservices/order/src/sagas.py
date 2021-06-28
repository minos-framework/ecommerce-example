"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
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


def _validate_products_callback(context: SagaContext) -> Model:
    product_ids = context["product_ids"]
    model = ModelType.build("ProductsQuery", {"ids": list[int]})(ids=product_ids)
    return model


def _exist_products_callback(value) -> None:
    if not value.exist:
        raise ValueError("One or more products do not exist.")


async def _create_commit_callback(context: SagaContext) -> SagaContext:
    product_ids = context["product_ids"]
    now = datetime.now()
    status = "created"
    order = await Order.create(product_ids, status, created_at=now, updated_at=now)
    context["order"] = order
    return context


CREATE_ORDER = (
    Saga("CreateOrder")
    .step()
    .invoke_participant("ValidateProducts", _validate_products_callback)
    .on_reply("_", _exist_products_callback)
    .commit(_create_commit_callback)
)
