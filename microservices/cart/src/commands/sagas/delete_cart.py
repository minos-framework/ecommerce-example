"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from collections import defaultdict

from minos.common import Model
from minos.saga import (
    Saga,
    SagaContext,
)

from .callbacks import _ReserveProductsQuery


def _reserve_products(context: SagaContext) -> Model:
    cart = context["cart"]
    quantities = defaultdict(int)
    for item in cart.entries:
        quantities[str(item.product)] += item.quantity

    return _ReserveProductsQuery(quantities=quantities)


def _release_products(context: SagaContext) -> Model:
    cart = context["cart"]
    quantities = defaultdict(int)
    for item in cart.entries:
        quantities[str(item.product)] -= item.quantity

    return _ReserveProductsQuery(quantities=quantities)


async def _create_cart(context: SagaContext) -> SagaContext:
    cart = context["cart"]
    result = await cart.delete()
    return SagaContext(result=result)


DELETE_CART = (
    Saga("DeleteCart")
    .step()
    .invoke_participant("ReserveProducts", _reserve_products)
    .with_compensation("ReserveProducts", _release_products)
    .commit(_create_cart)
)
