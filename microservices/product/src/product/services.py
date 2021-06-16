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
    """Ticket Service class"""

    @staticmethod
    async def create_product(
        product_code: str, title: str, description: str, price: int
    ) -> Product:
        """
        Creates a product

        :param product_code: Unique str representing the product
        :param title: Detailed nome of the product
        :param description: Additional considerations
        :param price: Price in €
        """
        return await Product.create(product_code, title, description, price)

    @staticmethod
    async def get_products(ids: list[int]) -> list[Product]:
        """Get a list of tickets.

        :param ids: List of ticket identifiers.
        :return: A list of ``Ticket`` instances.
        """
        return await Product.get(ids=ids)
