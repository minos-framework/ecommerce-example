"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import NoReturn
from uuid import UUID

from minos.common import (
    MinosSnapshotAggregateNotFoundException,
    MinosSnapshotDeletedAggregateException,
    ModelType,
    Request,
    Response,
    ResponseException,
)

from .services import (
    ProductService,
)

_Query = ModelType.build("Query", {"uuids": list[UUID]})


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
        try:
            content = await request.content(model_type=_Query)
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        try:
            products = await ProductService().get_products(**content)
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting products: {exc!r}")

        return Response(products)

    @staticmethod
    async def delete_product(request: Request) -> NoReturn:
        """TODO

        :param request: TODO
        :return: TODO
        """
        content = await request.content()

        try:
            await ProductService().delete_product(**content)
        except (MinosSnapshotDeletedAggregateException, MinosSnapshotAggregateNotFoundException):
            raise ResponseException(f"The product does not exist.")

    @staticmethod
    async def reserve_products(request: Request) -> NoReturn:
        """Reserve the requested quantities of products.

        :param: request: The ``Request`` instance that contains the quantities dictionary.
        :return: A ``Response containing a ``ValidProductInventoryList`` DTO.
        """
        content = await request.content()
        quantities = {UUID(k): v for k, v in content.quantities.items()}

        try:
            await ProductService().reserve_products(quantities)
        except (MinosSnapshotAggregateNotFoundException, MinosSnapshotDeletedAggregateException) as exc:
            raise ResponseException(f"Some products do not exist: {exc!r}")
        except Exception as exc:
            raise ResponseException(f"There is not enough product amount: {exc!r}")
