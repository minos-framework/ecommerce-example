"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""

from minos.common import (
    Service, MinosRepositoryAggregateNotFoundException, MinosRepositoryException,
)

from .aggregates import (
    Inventory,
    Product,
)


class ProductService(Service):
    """Product Service class"""

    async def create_product(self, code: str, title: str, description: str, price: float) -> Product:
        """Create a product.

        :param code: External product identifier.
        :param title: Name of the product.
        :param description: Description of the product.
        :param price: Price of the product.
        :return: A ``Product`` instance.
        """
        inventory = Inventory(amount=0)
        product = await Product.create(code, title, description, price, inventory)
        # await self.saga_manager.run("_CreateProduct", context=SagaContext(product=product))
        return product

    @staticmethod
    async def get_products(ids: list[int]) -> list[Product]:
        """Get a list of products.

        :param ids: List of product identifiers.
        :return: A list of ``Product`` instances.
        """
        values = {v.id: v async for v in Product.get(ids=ids)}
        return [values[id] for id in ids]

    @staticmethod
    async def update_inventory(product_id: int, amount: int) -> Product:
        """Update inventory with a difference.

        :param product_id: Identifier of the product.
        :param amount: Amount to be set.
        :return: The updated product instance.
        """
        product = await Product.get_one(product_id)
        product.inventory.amount = amount
        await product.save()
        return product

    @staticmethod
    async def update_inventory_diff(product_id: int, amount_diff: int) -> Product:
        """Update inventory with a difference.

        :param product_id: Identifier of the product.
        :param amount_diff: Amount difference to be applied.
        :return: The updated product instance.
        """
        product = await Product.get_one(product_id)
        product.inventory.amount += amount_diff
        await product.save()
        return product

    @staticmethod
    async def validate_products(ids: list[int]) -> bool:
        """TODO

        :param ids: TODO
        :return: TODO
        """
        ids = list(set(ids))

        try:
            # noinspection PyStatementEffect
            v = [v async for v in Product.get(ids=ids)]
            return True
        except MinosRepositoryException:
            return False
