"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""

from minos.common import (
    Request,
    Response,
)

from .services import (
    InventoryService,
)


class InventoryController:
    """Ticket Controller class"""

    @staticmethod
    async def create_inventory(request: Request) -> Response:
        """TODO

        :param request:TODO
        :return: TODO
        """
        content = await request.content()
        product = await InventoryService().create_inventory(**content[0])
        return Response(product)

    @staticmethod
    async def get_inventories(request: Request) -> Response:
        """TODO

        :param request: TODO
        :return: TODO
        """
        content = await request.content()
        if len(content) and hasattr(content[0], "ids"):
            content = content[0].ids
        else:
            content = list(map(int, content))
        products = await InventoryService().get_inventories(content)
        return Response(products)
