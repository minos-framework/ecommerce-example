from typing import (
    Any,
)

from minos.saga import (
    Saga,
    SagaContext,
)

from ..aggregates import (
    Credentials,
)


def _validate_username(context: SagaContext):
    username = {"username": context["username"]}
    return username


def _create_customer(context: SagaContext) -> dict[str, Any]:
    return context["metadata"]


async def _create_credentials(context: SagaContext) -> SagaContext:
    username = context["username"]
    password = context["password"]

    if await Credentials.exists_username(username):
        raise Exception(f"The given username already exists: {username}")

    credentials = await Credentials.create(username, password, active=True)
    return SagaContext(credentials=credentials)


CREATE_CUSTOMER_SAGA = (
    Saga("FullLogin").step().invoke_participant("CreateCustomer", _create_customer).commit(_create_credentials)
)
