from minos.saga import (
    Saga,
    SagaContext,
)

from ..aggregates import (
    Credentials,
)


def _create_customer(context: SagaContext):
    customer = {"name": context["name"], "surname": context["surname"], "address": context["address"]}

    return customer


async def _create_credentials(context: SagaContext) -> SagaContext:
    username = context["username"]
    password = context["password"]
    credentials = await Credentials.create(username, password, active=True)
    return SagaContext(credentials=credentials)


CREATE_CUSTOMER_SAGA = (
    Saga("FullLogin").step().invoke_participant("CreateCustomer", _create_customer).commit(_create_credentials)
)
