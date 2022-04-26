from collections import (
    defaultdict,
)

from minos.common import (
    Inject,
    ModelType,
)
from minos.saga import (
    Saga,
    SagaContext,
    SagaRequest,
    SagaResponse,
)

from ...aggregates import (
    Cart,
    CartAggregate,
)

_ReserveProductsQuery = ModelType.build("ValidateProductsQuery", {"quantities": dict[str, int]})


@Inject()
async def _reserve_products(context: SagaContext, aggregate: CartAggregate) -> SagaRequest:
    product_uuids = [context["product_uuid"]]
    cart_id = context["cart_id"]
    quantities = defaultdict(int)
    cart = await Cart.get(cart_id)
    for product_id in product_uuids:
        quantities[str(product_id)] += get_product_quantity(cart, product_id)

    return SagaRequest("ReserveProducts", _ReserveProductsQuery(quantities=quantities))


# noinspection PyUnusedLocal
def _raise(context: SagaContext, response: SagaResponse) -> SagaContext:
    raise ValueError("Errored response must abort the execution!")


@Inject()
async def _release_products(context: SagaContext, aggregate: CartAggregate) -> SagaRequest:
    product_uuids = [context["product_uuid"]]
    cart_id = context["cart_id"]
    quantities = defaultdict(int)
    cart = await Cart.get(cart_id)
    for product_id in product_uuids:
        quantities[str(product_id)] -= get_product_quantity(cart, product_id)

    return SagaRequest("ReserveProducts", _ReserveProductsQuery(quantities=quantities))


@Inject()
async def _remove_cart_item(context: SagaContext, aggregate: CartAggregate) -> SagaContext:
    cart_id = context["cart_id"]
    product = context["product"]
    cart = await Cart.get(cart_id)
    cart.entries.discard(product)

    await cart.save()
    return SagaContext(cart=cart)


def get_product_quantity(cart: Cart, product: str):
    for key, value in cart.entries.data.items():
        if str(value.product) == product:
            return value.quantity
    return 0


REMOVE_CART_ITEM = (
    Saga().remote_step(_reserve_products).on_error(_raise).on_failure(_release_products).commit(_remove_cart_item)
)
