"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from collections import defaultdict
from minos.common import (
    Model,
    ModelType,
)
from minos.saga import (
    Saga,
    SagaContext,
)
from src.aggregates import (
    Cart,
    CartItem,
)

_ReserveProductsQuery = ModelType.build("ValidateProductsQuery", {"quantities": dict[str, int]})


def _reserve_products_callback(context: SagaContext) -> Model:
    product_ids = [context["product_id"]]
    quantities = defaultdict(int)
    for product_id in product_ids:
        quantities[str(product_id)] += 1

    return _ReserveProductsQuery(quantities=quantities)


def _release_products_callback(context: SagaContext) -> Model:
    product_ids = [context["product_id"]]
    quantities = defaultdict(int)
    for product_id in product_ids:
        quantities[str(product_id)] -= 1

    return _ReserveProductsQuery(quantities=quantities)


async def _create_commit_callback(context: SagaContext) -> SagaContext:
    cart_id = context["cart_id"]
    product_id = context["product_id"]
    quantity = context["quantity"]
    cart = await Cart.get_one(cart_id)
    cart_item = CartItem(product=product_id, quantity=quantity)
    cart.products.append(cart_item)
    await cart.save()
    return SagaContext(cart=cart)


ADD_CART_ITEM = (
    Saga("AddCartItem")
    .step()
    .invoke_participant("ReserveProducts", _reserve_products_callback)
    .with_compensation("ReserveProducts", _release_products_callback)
    .commit(_create_commit_callback)
)
