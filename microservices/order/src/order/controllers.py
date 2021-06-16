"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""

from minos.common import (
    Request,
    Response,
)

from .dto import (
    ProductDto,
    ProductsQueryDto,
)
from .services import (
    ProductService,
    OrderService,
)


class OrderController:
    """Ticket Controller class"""

    @staticmethod
    async def create_order(request: Request) -> Response:
        """TODO

        :param request:TODO
        :return: TODO
        """
        content = await request.content()
        order = await OrderService().create_order(**content[0])
        return Response(order)

    @staticmethod
    async def get_orders(request: Request) -> Response:
        """TODO

        :param request: TODO
        :return: TODO
        """
        content = await request.content()
        if len(content) and isinstance(content[0], ProductsQueryDto):
            content = content[0].ids
        orders = [
            ProductDto.from_dict(order.avro_data)
            for order in await OrderService().get_orders(content)
        ]
        return Response(orders)
