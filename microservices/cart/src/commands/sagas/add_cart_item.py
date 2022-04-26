from minos.common import (
    Inject,
)
from minos.saga import (
    Saga,
    SagaContext,
    SagaResponse,
)

from ...aggregates import (
    Cart,
    CartAggregate,
    CartEntry,
)
from .callbacks import (
    _release_products,
    _reserve_products,
)


# noinspection PyUnusedLocal
def _raise(context: SagaContext, response: SagaResponse) -> SagaContext:
    raise ValueError("Errored response must abort the execution!")


@Inject()
async def _create_cart_item(context: SagaContext, aggregate: CartAggregate) -> SagaContext:
    cart_id = context["cart_id"]
    product_uuid = context["product_uuid"]
    quantity = context["quantity"]
    cart = await Cart.get(cart_id)
    cart_item = CartEntry(product=product_uuid, quantity=quantity)
    cart.entries.add(cart_item)
    await cart.save()
    return SagaContext(cart=cart)


ADD_CART_ITEM = (
    Saga().remote_step(_reserve_products).on_error(_raise).on_failure(_release_products).commit(_create_cart_item)
)
