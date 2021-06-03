"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""


from minos.microservice import (
    Service,
)

from .aggregates import (
    Product,
)


class ProductService(Service):
    """Ticket Service class"""

    @staticmethod
    async def create_product(external_id: int, name: str, description: str, brand: str, unit_price: float) -> Product:
        """Create a product.

        :param external_id: TODO.
        :param name: TODO.
        :param description: TODO.
        :param brand: TODO.
        :param unit_price: TODO.
        :return: TODO.
        """
        return await Product.create(external_id, name, description, brand, unit_price)

    @staticmethod
    async def get_products(ids: list[int]) -> list[Product]:
        """Get a list of tickets.

        :param ids: List of ticket identifiers.
        :return: A list of ``Ticket`` instances.
        """
        return await Product.get(ids=ids)
