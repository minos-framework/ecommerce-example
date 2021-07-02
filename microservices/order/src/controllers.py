"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import (
    Request,
    Response,
    ModelType,
)

from .services import (
    OrderService,
)

_Query = ModelType.build("Query", {"ids": list[int]})


class OrderController:
    """Ticket Controller class"""

    @staticmethod
    async def create_order(request: Request) -> Response:
        """Create a new ``Order`` instance.

        :param request: The ``Request`` containing the list of product identifiers to be included in the ``Order``.
        :return: A ``Response`` containing the ``UUID`` that identifies the ``SagaExecution``.
        """
        content = await request.content()
        uuid = await OrderService().create_order(**content)
        return Response(str(uuid))

    @staticmethod
    async def get_orders(request: Request) -> Response:
        """Get a list of orders by id.

        :param request: The ``Request`` instance containing the list of ``Order`` identifiers.
        :return: A ``Response`` containing the list of ``Order`` instances.
        """
        content = await request.content(model_type=_Query)
        orders = await OrderService().get_orders(**content)
        return Response(orders)
