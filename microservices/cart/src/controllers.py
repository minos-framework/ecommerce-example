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

from .services import CartService

_Query = ModelType.build("Query", {"ids": list[int]})


class CartController:
    """Ticket Controller class"""

    @staticmethod
    async def create_cart(request: Request) -> Response:
        """Create a new cart.

        :param request: The ``Request`` instance to be use to compute the price.
        :return: A ``Response`` containing the created ticket.
        """
        content = await request.content()
        cart = await CartService().create_cart(**content)
        return Response(cart)

    @staticmethod
    async def add_item(request: Request) -> Response:
        """Create a new cart.

        :param request: The ``Request`` instance to be use to compute the price.
        :return: A ``Response`` containing the created ticket.
        """
        content = await request.content()
        cart = await CartService().add_item(**content)
        return Response(cart)

    @staticmethod
    async def delete_item(request: Request) -> Response:
        pass

    @staticmethod
    async def update_item(request: Request) -> Response:
        pass

    @staticmethod
    async def get_cart(request: Request) -> Response:
        pass

    @staticmethod
    async def delete_cart(request: Request) -> Response:
        pass
