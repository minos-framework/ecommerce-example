"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import (
    UUID,
)

from minos.common import (
    Request,
    Response,
)

from .dto import ProductsQueryDto
from .services import (
    ShipmentService,
)


class ShipmentController:
    """TODO"""

    async def create_shipment(self, request: Request) -> Response:
        """TODO"""
        content = await request.content()

        products_query = ProductsQueryDto(content[0]["product_ids"])
        uuid: UUID = await ShipmentService().create_shipment(products_query=products_query)
        return Response(str(uuid))

    async def get_shipments(self, request: Request) -> Response:
        """TODO"""
        content = await request.content()
        shipments = await ShipmentService().get_shipments(content)
        return Response(shipments)
