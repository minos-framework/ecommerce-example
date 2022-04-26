from collections import (
    defaultdict,
)

from minos.common import (
    Inject,
)
from minos.saga import (
    Saga,
    SagaContext,
    SagaRequest,
    SagaResponse,
)

from ...aggregates import (
    CartAggregate,
)
from .callbacks import (
    _ReserveProductsQuery,
)


def _reserve_products(context: SagaContext) -> SagaRequest:
    cart = context["cart"]
    quantities = defaultdict(int)
    for item in cart.entries:
        quantities[str(item.product)] += item.quantity

    return SagaRequest("ReserveProducts", _ReserveProductsQuery(quantities))


# noinspection PyUnusedLocal
def _raise(context: SagaContext, response: SagaResponse) -> SagaContext:
    raise ValueError("Errored response must abort the execution!")


def _release_products(context: SagaContext) -> SagaRequest:
    cart = context["cart"]
    quantities = defaultdict(int)
    for item in cart.entries:
        quantities[str(item.product)] -= item.quantity

    return SagaRequest("ReserveProducts", _ReserveProductsQuery(quantities))


@Inject()
async def _create_cart(context: SagaContext, aggregate: CartAggregate) -> SagaContext:
    cart = context["cart"]
    result = await cart.delete()
    return SagaContext(result=result)


DELETE_CART = Saga().remote_step(_reserve_products).on_error(_raise).on_failure(_release_products).commit(_create_cart)
