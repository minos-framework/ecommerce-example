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
        product = await ProductService().create_product(**content)
        return Response(product)

    @staticmethod
    async def update_inventory(request: Request) -> Response:
        """Update inventory amount with a difference.

        :param request: ``Request`` that contains the needed information.
        :return: ``Response`` containing the updated product.
        """
        content = await request.content()
        product = await ProductService().update_inventory(**content)
        return Response(product)

    @staticmethod
    async def update_inventory_diff(request: Request) -> Response:
        """Update inventory amount with a difference.

        :param request: ``Request`` that contains the needed information.
        :return: ``Response`` containing the updated product.
        """
        content = await request.content()
        product = await ProductService().update_inventory_diff(**content)
        return Response(product)

    @staticmethod
    async def get_products(request: Request) -> Response:
        """Get products.

        :param request: The ``Request`` instance that contains the product identifiers.
        :return: A ``Response`` instance containing the requested products.
        """
        content = await request.content()
        ids = list(map(int, content["ids"]))
        products = await ProductService().get_products(ids)
        return Response(products)

    @staticmethod
    async def validate_products(request: Request) -> Response:
        """Check if the list of passed products is valid.

        :param: request: The ``Request`` containing the list of identifiers.
        :return: A ``Response containing a ``ValidProductList`` DTO.
        """
        content = await request.content()
        exist = await ProductService().validate_products(**content)
        model = ModelType.build("ValidProductList", {"exist": bool})(exist=exist)
        return Response(model)

    @staticmethod
    async def reserve_products(request: Request) -> Response:
        """Reserve the requested quantities of products.

        :param: request: The ``Request`` instance that contains the quantities dictionary.
        :return: A ``Response containing a ``ValidProductInventoryList`` DTO.
        """
        content = await request.content()
        quantities = {int(k): v for k, v in content.quantities.items()}
        exist = await ProductService().reserve_products(quantities)
        model = ModelType.build("ValidProductInventoryList", {"exist": bool})(exist=exist)
        return Response(model)
