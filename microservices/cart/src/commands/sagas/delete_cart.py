"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from collections import (
    defaultdict,
)
from .callbacks import (
    _ReserveProductsQuery,
)
from minos.common import (
    Model,
)
from minos.saga import (
    Saga,
    SagaContext,
)


def _reserve_products_callback(context: SagaContext) -> Model:
    cart = context["cart"]
    quantities = defaultdict(int)
    for item in cart.products:
        quantities[str(item.product)] += item.quantity

    return _ReserveProductsQuery(quantities=quantities)


def _release_products_callback(context: SagaContext) -> Model:
    cart = context["cart"]
    quantities = defaultdict(int)
    for item in cart.products:
        quantities[str(item.product)] -= item.quantity

    return _ReserveProductsQuery(quantities=quantities)


async def _create_commit_callback(context: SagaContext) -> SagaContext:
    cart = context["cart"]
    result = await cart.delete()
    return SagaContext(result=result)


DELETE_CART = (
    Saga("DeleteCart")
    .step()
    .invoke_participant("ReserveProducts", _release_products_callback)
    .with_compensation("ReserveProducts", _reserve_products_callback)
    .commit(_create_commit_callback)
)
