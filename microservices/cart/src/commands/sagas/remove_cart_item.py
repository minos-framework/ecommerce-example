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
from src.aggregates import Cart


_ReserveProductsQuery = ModelType.build("ValidateProductsQuery", {"quantities": dict[str, int]})


async def _reserve_products_callback(context: SagaContext) -> Model:
    product_uuids = [context["product_uuid"]]
    cart_id = context["cart_id"]
    quantities = defaultdict(int)
    cart = await Cart.get_one(cart_id)
    for product_id in product_uuids:
        quantities[str(product_id)] += get_product_quantity(cart, product_id)

    return _ReserveProductsQuery(quantities=quantities)


async def _release_products_callback(context: SagaContext) -> Model:
    product_uuids = [context["product_uuid"]]
    cart_id = context["cart_id"]
    quantities = defaultdict(int)
    cart = await Cart.get_one(cart_id)
    for product_id in product_uuids:
        quantities[str(product_id)] -= get_product_quantity(cart, product_id)

    return _ReserveProductsQuery(quantities=quantities)


async def _create_commit_callback(context: SagaContext) -> SagaContext:
    cart_id = context["cart_id"]
    product = context["product"]
    cart = await Cart.get_one(cart_id)
    cart.products.discard(product)

    await cart.save()
    return SagaContext(cart=cart)


def get_product_quantity(cart: Cart, product: str):
    for key, value in cart.products.data.items():
        if str(value.product) == product:
            return value.quantity
    return 0


REMOVE_CART_ITEM = (
    Saga("RemoveCartItem")
    .step()
    .invoke_participant("ReserveProducts", _release_products_callback)
    .with_compensation("ReserveProducts", _reserve_products_callback)
    .commit(_create_commit_callback)
)
