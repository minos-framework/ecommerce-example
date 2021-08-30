from collections import (
    defaultdict,
)
from uuid import (
    UUID,
)

from minos.common import (
    Aggregate,
    Model,
    ModelType,
)
from minos.saga import (
    Saga,
    SagaContext,
)

from ..aggregates import (
    Customer,
)

CreateCustomerQuery = ModelType.build("CreateCustomerQuery", {"quantities": dict[str, int]})


def _create_customer(context: SagaContext) -> Model:
    product_uuids = context["product_uuids"]
    quantities = defaultdict(int)
    for product_uuid in product_uuids:
        quantities[str(product_uuid)] += 1

    return CreateCustomerQuery(quantities)


def _revert_create_customer(context: SagaContext) -> Model:
    product_uuids = context["product_uuids"]
    quantities = defaultdict(int)
    for product_uuid in product_uuids:
        quantities[str(product_uuid)] -= 1

    return CreateCustomerQuery(quantities)


async def _create_commit_callback(context: SagaContext) -> SagaContext:
    product_uuids = context["product_uuids"]
    ticket_uuid = context["ticket_uuid"]
    status = "created"
    customer = await Customer.create(product_uuids, ticket_uuid, status)
    return SagaContext(customer=customer)


CREATE_CUSTOMER = (
    Saga("FullLogin")
    .step()
    .invoke_participant("CreateCustomer", _create_customer)
    .with_compensation("CreateCustomer", _revert_create_customer)
    .commit(_create_commit_callback)
)