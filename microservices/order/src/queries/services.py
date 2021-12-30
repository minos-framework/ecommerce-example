from dependency_injector.wiring import (
    Provide,
)
from minos.aggregate import (
    AggregateDiff,
)
from minos.common import (
    UUID_REGEX,
)
from minos.cqrs import (
    QueryService,
)
from minos.networks import (
    Request,
    Response,
    ResponseException,
    RestRequest,
    enroute,
)

from .repositories import (
    OrderQueryRepository,
)


class OrderQueryService(QueryService):
    """Order Query Service class."""

    repository: OrderQueryRepository = Provide["order_repository"]

    @enroute.broker.query("GetOrderQRS")
    @enroute.rest.query(f"/orders/{{uuid:{UUID_REGEX.pattern}}}", "GET")
    async def get_order(self, request: Request) -> Response:
        """Get order.

        :param request: The ``Request`` instance that contains the order identifier.
        :return: A ``Response`` instance containing the requested order.
        """

        if isinstance(request, RestRequest):
            uuid = (await request.params())["uuid"]
        else:
            content = await request.content()
            uuid = content["uuid"]

        try:
            order = await self.repository.get(uuid)
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        return Response(order)

    @enroute.broker.query("GetUserOrders")
    @enroute.rest.query(f"/orders/user/{{uuid:{UUID_REGEX.pattern}}}", "GET")
    async def get_user_orders(self, request: Request) -> Response:
        """Get user orders.

        :param request: The ``Request`` instance that contains the order identifier.
        :return: A ``Response`` instance containing the requested order.
        """
        if isinstance(request, RestRequest):
            params = await request.params()
            uuid = params["uuid"]
        else:
            content = await request.content()
            uuid = content["uuid"]

        try:
            order = await self.repository.get_by_user(uuid)
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        return Response(order)

    @enroute.broker.event("OrderCreated")
    async def order_created(self, request: Request) -> None:
        """Handle the order creation events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        await self.repository.create(
            uuid=diff.uuid,
            version=diff.version,
            created_at=diff.created_at,
            updated_at=diff.created_at,
            **diff.fields_diff,
        )

    @enroute.broker.event("OrderUpdated")
    async def order_updated(self, request: Request) -> None:
        """Handle the order update events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        print(await request.content())

    @enroute.broker.event("OrderDeleted")
    async def order_deleted(self, request: Request) -> None:
        """Handle the order deletion events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        print(await request.content())
