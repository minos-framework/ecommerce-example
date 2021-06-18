"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import Request, Response

from .dto import ProductDto, ProductsQueryDto
from .services import ProductService


class ProductController:
    """Ticket Controller class"""

    @staticmethod
    async def create_product(request: Request) -> Response:
        """TODO

        :param request:TODO
        :return: TODO
        """
        content = await request.content()
        product = await ProductService().create_product(**content[0])
        return Response(product)

    @staticmethod
    async def get_products(request: Request) -> Response:
        """TODO

        :param request: TODO
        :return: TODO
        """
        content = await request.content()
        if len(content) and isinstance(content[0], ProductsQueryDto):
            content = content[0].ids
        products = [ProductDto.from_dict(product.avro_data) for product in await ProductService().get_products(content)]
        return Response(products)
