from __future__ import (
    annotations,
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

from ..aggregates import (
    Credentials,
    CredentialsAggregate,
)


def _validate_username(context: SagaContext):
    username = {"username": context["username"]}
    return username


def _send_create_customer(context: SagaContext) -> SagaRequest:
    return SagaRequest("CreateCustomer", context["metadata"])


async def _send_delete_customer(context: SagaContext) -> SagaRequest:
    return SagaRequest("DeleteCustomer", {"uuid": context["user"]})


async def _on_create_user_success(context: SagaContext, response: SagaResponse) -> SagaContext:
    user = await response.content()
    context["user"] = user.uuid
    return context


@Inject()
async def _create_credentials(context: SagaContext, aggregate: CredentialsAggregate) -> SagaContext:
    username = context["username"]
    password = context["password"]
    user = context["user"]

    credentials = await aggregate.create_credentials_instance(username, password, user=user)

    return SagaContext(credentials=credentials)


CREATE_CREDENTIALS_SAGA = (
    Saga()
    .remote_step(_send_create_customer)
    .on_success(_on_create_user_success)
    .on_failure(_send_delete_customer)
    .commit(_create_credentials)
)
