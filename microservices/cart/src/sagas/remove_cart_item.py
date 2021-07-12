"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from collections import (
    defaultdict,
)
from minos.common import (
    Model,
    ModelType,
)
from minos.saga import (
    Saga,
    SagaContext,
)
from src.aggregates import (
    Cart, CartItem,
)

_ReserveProductsQuery = ModelType.build("ValidateProductsQuery", {"quantities": dict[str, int]})


def _reserve_products_callback(context: SagaContext) -> Model:
    product = context["product"]
    quantities = defaultdict(int)
    quantities[str(product.id)] += product.quantity

    return _ReserveProductsQuery(quantities=quantities)


def _release_products_callback(context: SagaContext) -> Model:
    product = context["product"]
    quantities = defaultdict(int)
    quantities[str(product.id)] -= product.quantity

    return _ReserveProductsQuery(quantities=quantities)


async def _create_commit_callback(context: SagaContext) -> SagaContext:
    cart_id = context["cart_id"]
    idx = context["product_id"]
    cart = await Cart.get_one(cart_id)
    cart.products.pop(idx)

    await cart.save()
    return SagaContext(cart=cart)


REMOVE_CART_ITEM = (
    Saga("RemoveCartItem")
    .step()
    .invoke_participant("ReserveProducts", _release_products_callback)
    .with_compensation("ReserveProducts", _reserve_products_callback)
    .commit(_create_commit_callback)
)
