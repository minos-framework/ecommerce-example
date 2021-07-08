"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import (
    ModelType,
    Request,
    Response,
)

from .services import (
    CartService,
)

_Query = ModelType.build("Query", {"ids": list[int]})


class CartController:
    """Ticket Controller class"""

    @staticmethod
    async def add_items(request: Request) -> Response:
        """Create a new cart.

        :param request: The ``Request`` instance to be use to compute the price.
        :return: A ``Response`` containing the created ticket.
        """
        content = await request.content()
        cart = await CartService().add_items(**content)
        return Response(cart)
