"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import UUID

from minos.common import (
    ModelType,
    Request,
    Response,
    ResponseException,
    Service,
)
from minos.saga import SagaContext

from ..aggregates import Order


class OrderCommandService(Service):
    """Ticket Service class"""

    async def create_order(self, request: Request) -> Response:
        """Create a new ``Order`` instance.

        :param request: The ``Request`` containing the list of product identifiers to be included in the ``Order``.
        :return: A ``Response`` containing the ``UUID`` that identifies the ``SagaExecution``.
        """
        content = await request.content()
        product_uuids = content["product_uuids"]
        uuid = await self.saga_manager.run("CreateOrder", context=SagaContext(product_uuids=product_uuids))
        return Response(uuid)

    @staticmethod
    async def get_orders(request: Request) -> Response:
        """Get a list of orders by uuid.

        :param request: The ``Request`` instance containing the list of ``Order`` identifiers.
        :return: A ``Response`` containing the list of ``Order`` instances.
        """
        _Query = ModelType.build("Query", {"uuids": list[UUID]})
        try:
            content = await request.content(model_type=_Query)
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        uuids = content["uuids"]

        try:
            values = {v.uuid: v async for v in Order.get(uuids=uuids)}
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting orders: {exc!r}")
        orders = [values[uuid] for uuid in uuids]

        return Response(orders)
