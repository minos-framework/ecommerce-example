from typing import (
    Any,
)
from uuid import (
    UUID,
)

from minos.saga import (
    Saga,
    SagaContext,
)

from ..aggregates import (
    Credentials,
    Customer,
)


def _validate_username(context: SagaContext):
    username = {"username": context["username"]}
    return username


def _create_customer(context: SagaContext) -> dict[str, Any]:
    return context["metadata"]


def _on_reply(user: Customer) -> UUID:
    return user.uuid


async def _create_credentials(context: SagaContext) -> SagaContext:
    username = context["username"]
    password = context["password"]
    user = context["user"]

    if await Credentials.exists_username(username):
        raise Exception(f"The given username already exists: {username}")

    credentials = await Credentials.create(username, password, active=True, user=user)
    return SagaContext(credentials=credentials)


CREATE_CUSTOMER_SAGA = (
    Saga("FullLogin")
    .step()
    .invoke_participant("CreateCustomer", _create_customer)
    .on_reply("user", _on_reply)
    .commit(_create_credentials)
)
