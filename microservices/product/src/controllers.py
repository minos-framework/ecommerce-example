"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""

from minos.common import (
    Request,
    Response,
)
from minos.networks import HttpRequest

from .services import (
    ProductService,
)


class ProductController:
    """Product Controller class"""

    @staticmethod
    async def create_product(request: Request) -> Response:
        """Create a new product instance.

        :param request: The ``Request`` that contains the needed information to create the product.
        :return: A ``Response`` containing the already created product.
        """
        content = await request.content()
        product = await ProductService().create_product(**content[0])
        return Response(product)

    @staticmethod
    async def update_inventory(request: Request) -> Response:
        """Update inventory amount with a difference.

        :param request: ``Request`` that contains the needed information.
        :return: ``Response`` containing the updated product.
        """
        content = await request.content()

        # FIXME: This should be performed internally by the framework.
        if isinstance(request, HttpRequest):
            content[0]["product_id"] = int(request.raw_request.match_info['product_id'])  # FIXME

        product = await ProductService().update_inventory(**content[0])
        return Response(product)

    @staticmethod
    async def update_inventory_diff(request: Request) -> Response:
        """Update inventory amount with a difference.

        :param request: ``Request`` that contains the needed information.
        :return: ``Response`` containing the updated product.
        """
        content = await request.content()

        # FIXME: This should be performed internally by the framework.
        if isinstance(request, HttpRequest):
            content[0]["product_id"] = int(request.raw_request.match_info['product_id'])

        product = await ProductService().update_inventory_diff(**content[0])
        return Response(product)

    @staticmethod
    async def get_products(request: Request) -> Response:
        """Get products.

        :param request: The ``Request`` instance that contains the product identifiers.
        :return: A ``Response`` instance containing the requested products.
        """
        content = await request.content()
        if len(content) and hasattr(content[0], "ids"):
            content = content[0].ids
        else:
            content = list(map(int, content))
        products = await ProductService().get_products(content)
        return Response(products)
