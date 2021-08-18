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
from minos.saga import SagaContext

_ReserveProductsQuery = ModelType.build("ValidateProductsQuery", {"quantities": dict[str, int]})


def _reserve_products_callback(context: SagaContext) -> Model:
    product_uuids = [context["product_uuid"]]
    quantities = defaultdict(int)
    for product_id in product_uuids:
        quantities[str(product_id)] += context["quantity"]

    return _ReserveProductsQuery(quantities=quantities)


def _release_products_callback(context: SagaContext) -> Model:
    product_uuids = [context["product_uuid"]]
    quantities = defaultdict(int)
    for product_id in product_uuids:
        quantities[str(product_id)] -= context["quantity"]

    return _ReserveProductsQuery(quantities=quantities)
