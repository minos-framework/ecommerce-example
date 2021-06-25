"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""

from minos.common import (
    Service,
)

from .aggregates import (
    Product,
)


class ProductService(Service):
    """Product Service class"""

    @staticmethod
    async def create_product(code: str, title: str, description: str, price: float) -> Product:
        """Create a product.

        :param code: External product identifier.
        :param title: Name of the product.
        :param description: Description of the product.
        :param price: Price of the product.
        :return: A ``Product`` instance.
        """
        return await Product.create(code, title, description, price)

    @staticmethod
    async def get_products(ids: list[int]) -> list[Product]:
        """Get a list of products.

        :param ids: List of product identifiers.
        :return: A list of ``Product`` instances.
        """
        values = {v.id: v async for v in Product.get(ids=ids)}
        return [values[id] for id in ids]
