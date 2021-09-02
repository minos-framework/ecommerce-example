"""src.queries.services module."""

from uuid import (
    UUID,
)

from dependency_injector.wiring import (
    Provide,
)
from minos.common import (
    UUID_REGEX,
    AggregateDiff,
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

from .repositories import (
    OrderQueryRepository,
)
from .. import PaymentDetail, ShipmentDetail


class OrderQueryService(QueryService):
    """Order Query Service class."""

    repository: OrderQueryRepository = Provide["order_repository"]

    @staticmethod
    @enroute.broker.query("GetOrders")
    @enroute.rest.query("/orders", "GET")
    async def get_orders(request: Request) -> Response:
        """Get orders.

        :param request: The ``Request`` instance that contains the order identifiers.
        :return: A ``Response`` instance containing the requested orders.
        """
        try:
            content = await request.content(model_type=ModelType.build("Query", {"uuids": list[UUID]}))
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        try:
            from ..aggregates import (
                Order,
            )

            iterable = Order.get(uuids=content["uuids"])
            values = {v.uuid: v async for v in iterable}
            orders = [values[uuid] for uuid in content["uuids"]]
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting orders: {exc!r}")

        return Response(orders)

    @enroute.broker.query("GetOrder")
    @enroute.rest.query(f"/orders/{{uuid:{UUID_REGEX.pattern}}}", "GET")
    async def get_order(self, request: Request) -> Response:
        """Get order.

        :param request: The ``Request`` instance that contains the order identifier.
        :return: A ``Response`` instance containing the requested order.
        """
        content = await request.content()
        try:
            order = await self.repository.get(content["uuid"])

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
        content = await request.content()
        try:
            order = await self.repository.get_by_user(content["uuid"])

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
