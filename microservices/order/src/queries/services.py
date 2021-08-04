"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import NoReturn
from uuid import UUID

from minos.common import (
    UUID_REGEX,
    ModelType,
)
from minos.cqrs import QueryService
from minos.networks import (
    Request,
    Response,
    ResponseException,
    enroute,
)


class OrderQueryService(QueryService):
    """Order Query Service class."""

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
            from ..aggregates import Order

            iterable = Order.get(uuids=content["uuids"])
            values = {v.uuid: v async for v in iterable}
            orders = [values[uuid] for uuid in content["uuids"]]
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting orders: {exc!r}")

        return Response(orders)

    @staticmethod
    @enroute.broker.query("GetOrder")
    @enroute.rest.query(f"/orders/{{uuid:{UUID_REGEX.pattern}}}", "GET")
    async def get_order(request: Request) -> Response:
        """Get order.

        :param request: The ``Request`` instance that contains the order identifier.
        :return: A ``Response`` instance containing the requested order.
        """
        try:
            content = await request.content(model_type=ModelType.build("Query", {"uuid": UUID}))
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        try:
            from ..aggregates import Order

            order = await Order.get_one(content["uuid"])
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting the order: {exc!r}")

        return Response(order)

    @enroute.broker.event("OrderCreated")
    async def order_created(self, request: Request) -> NoReturn:
        """Handle the order creation events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        print(await request.content())

    @enroute.broker.event("OrderUpdated")
    async def order_updated(self, request: Request) -> NoReturn:
        """Handle the order update events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        print(await request.content())

    @enroute.broker.event("OrderDeleted")
    async def order_deleted(self, request: Request) -> NoReturn:
        """Handle the order deletion events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        print(await request.content())
