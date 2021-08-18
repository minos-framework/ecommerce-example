"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import (
    NoReturn,
)
from uuid import (
    UUID,
)

from minos.common import (
    UUID_REGEX,
    MinosSnapshotAggregateNotFoundException,
    MinosSnapshotDeletedAggregateException,
)
from minos.cqrs import (
    CommandService,
)
from minos.networks import (
    Request,
    Response,
    ResponseException,
    enroute,
)

from ..aggregates import (
    Product,
)


class ReviewCommandService(CommandService):
    """Product Service class"""

    @staticmethod
    @enroute.broker.command("CreateProduct")
    @enroute.rest.command("/products", "POST")
    async def create_product(request: Request) -> Response:
        """Create a new product instance.

        :param request: The ``Request`` that contains the needed information to create the product.
        :return: A ``Response`` containing the already created product.
        """
        content = await request.content()
        title = content["title"]
        description = content["description"]
        price = content["price"]

        product = await Product.create(title, description, price)

        return Response(product)
