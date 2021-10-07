from collections import (
    defaultdict,
)

from minos.common import (
    ModelType,
)
from minos.saga import (
    Saga,
    SagaContext,
    SagaRequest,
    SagaResponse,
)

from src.aggregates import (
    Cart,
)

_ReserveProductsQuery = ModelType.build("ValidateProductsQuery", {"quantities": dict[str, int]})


async def _release_or_reserve_products(context: SagaContext) -> SagaRequest:
    product_uuids = [context["product_uuid"]]
    quantities = defaultdict(int)
    cart_id = context["cart_id"]
    quantity = context["quantity"]

    for product_id in product_uuids:
        prev = await Cart.get(cart_id)

        prev_quantity = 0
        for key, value in prev.entries.data.items():
            if str(value.product) == product_id:
                prev_quantity = value.quantity

        q = prev_quantity - quantity

        if q == 0:
            quantities[str(product_id)] += 0
        else:
            if q > 0:
                quantities[str(product_id)] -= abs(q)
            else:
                quantities[str(product_id)] += abs(q)

    return SagaRequest("ReserveProducts", _ReserveProductsQuery(quantities=quantities))


# noinspection PyUnusedLocal
def _raise(context: SagaContext, response: SagaResponse) -> SagaContext:
    raise ValueError("Errored response must abort the execution!")


async def _compensation(context: SagaContext) -> SagaRequest:
    product_uuids = [context["product_uuid"]]
    quantities = defaultdict(int)
    cart_id = context["cart_id"]
    quantity = context["quantity"]

    for product_id in product_uuids:
        prev = await Cart.get(cart_id)

        prev_quantity = 0
        for key, value in prev.entries.data.items():
            if str(value.product) == product_id:
                prev_quantity = value.quantity

        q = prev_quantity - quantity

        if q == 0:
            quantities[str(product_id)] += 0
        else:
            if q > 0:
                quantities[str(product_id)] += abs(q)
            else:
                quantities[str(product_id)] -= abs(q)

    return SagaRequest("ReserveProducts", _ReserveProductsQuery(quantities=quantities))


async def _update_cart_item(context: SagaContext) -> SagaContext:
    cart_id = context["cart_id"]
    product_uuid = context["product_uuid"]
    quantity = context["quantity"]
    cart = await Cart.get(cart_id)

    for key, value in cart.entries.data.items():
        if str(value.product) == product_uuid:
            value.quantity = quantity

    await cart.save()
    return SagaContext(cart=cart)


UPDATE_CART_ITEM = (
    Saga().step(_release_or_reserve_products).on_error(_raise).on_failure(_compensation).commit(_update_cart_item)
)
