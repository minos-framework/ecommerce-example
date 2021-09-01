from minos.saga import (
    Saga,
    SagaContext,
)

from ..aggregates import (
    Credentials,
)


def _validate_username(context: SagaContext):
    username = context["username"]
    return username


def _create_customer(context: SagaContext):
    customer = {"name": context["name"], "surname": context["surname"], "address": context["address"]}

    return customer


async def _create_credentials(context: SagaContext) -> SagaContext:
    username = context["username"]
    password = context["password"]
    credentials = await Credentials.create(username, password, active=True)
    return SagaContext(credentials=credentials)


CREATE_CUSTOMER_SAGA = Saga("FullLogin") \
    .step() \
    .invoke_participant("GetByUsername", _validate_username) \
    .step() \
    .invoke_participant("CreateCustomer", _create_customer) \
    .commit(_create_credentials)
