"""src.queries.services module."""

from uuid import (
    UUID,
)

from minos.common import (
    ModelType,
)
from minos.cqrs import (
    QueryService,
)
from minos.networks import (
    Request,
    Response,
    ResponseException,
    enroute,
)


class CustomerQueryService(QueryService):
    """Customer Query Service class"""

    @staticmethod
    @enroute.broker.query("GetCustomers")
    async def get_customer(request: Request) -> Response:
        """Get Customers.

        :param request: The ``Request`` instance that contains the user identifiers.
        :return: A ``Response`` instance containing the requested users.
        """
        try:
            content = await request.content(model_type=ModelType.build("Query", {"uuids": list[UUID]}))
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        try:
            from ..aggregates import (
                Customer,
            )

            iterable = Customer.get(uuids=content["uuids"])
            values = {v.uuid: v async for v in iterable}
            users = [values[uuid] for uuid in content["uuids"]]
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting users: {exc!r}")

        return Response(users)

    @staticmethod
    @enroute.broker.query("GetCustomer")
    async def get_customer(request: Request) -> Response:
        """Get Customer.

        :param request: The ``Request`` instance that contains the user identifier.
        :return: A ``Response`` instance containing the requested user.
        """
        try:
            content = await request.content(model_type=ModelType.build("Query", {"uuid": UUID}))
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        try:
            from ..aggregates import (
                Customer,
            )

            user = await Customer.get_one(content["uuid"])
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting the user: {exc!r}")

        return Response(user)
