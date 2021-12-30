from collections import (
    defaultdict,
)

from minos.common import (
    ModelType,
)
from minos.saga import (
    SagaContext,
    SagaRequest,
)

_ReserveProductsQuery = ModelType.build("ValidateProductsQuery", {"quantities": dict[str, int]})


def _reserve_products(context: SagaContext) -> SagaRequest:
    product_uuids = [context["product_uuid"]]
    quantities = defaultdict(int)
    for product_id in product_uuids:
        quantities[str(product_id)] += context["quantity"]

    return SagaRequest("ReserveProducts", _ReserveProductsQuery(quantities))


def _release_products(context: SagaContext) -> SagaRequest:
    product_uuids = [context["product_uuid"]]
    quantities = defaultdict(int)
    for product_id in product_uuids:
        quantities[str(product_id)] -= context["quantity"]

    return SagaRequest("ReserveProducts", _ReserveProductsQuery(quantities))
