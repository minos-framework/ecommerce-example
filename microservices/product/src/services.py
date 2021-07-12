"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import (
    NoReturn,
)
from uuid import (
    UUID, uuid4,
)

from minos.common import (
    Service,
)

from .aggregates import (
    Inventory,
    Product,
)


class ProductService(Service):
    """Product Service class"""

    @staticmethod
    async def create_product(title: str, description: str, price: float) -> Product:
        """Create a product.

        :param title: Name of the product.
        :param description: Description of the product.
        :param price: Price of the product.
        :return: A ``Product`` instance.
        """
        code = uuid4().hex.upper()[0:6]
        inventory = Inventory(amount=0)
        product = await Product.create(code, title, description, price, inventory)
        # await self.saga_manager.run("_CreateProduct", context=SagaContext(product=product))
        return product

    @staticmethod
    async def get_products(uuids: list[UUID]) -> list[Product]:
        """Get a list of products.

        :param uuids: List of product identifiers.
        :return: A list of ``Product`` instances.
        """
        values = {v.uuid: v async for v in Product.get(uuids=uuids)}
        return [values[uuid] for uuid in uuids]

    @staticmethod
    async def delete_product(uuid: UUID) -> NoReturn:
        """TODO

        :param uuid: TODO
        :return: TODO
        """
        product = await Product.get_one(uuid)
        await product.delete()

    @staticmethod
    async def update_inventory(uuid: UUID, amount: int) -> Product:
        """Update inventory with a difference.

        :param uuid: Identifier of the product.
        :param amount: Amount to be set.
        :return: The updated product instance.
        """
        product = await Product.get_one(uuid)
        product.inventory.amount = amount
        await product.save()
        return product

    @staticmethod
    async def update_inventory_diff(uuid: UUID, amount_diff: int) -> Product:
        """Update inventory with a difference.

        :param uuid: Identifier of the product.
        :param amount_diff: Amount difference to be applied.
        :return: The updated product instance.
        """
        product = await Product.get_one(uuid)
        product.inventory.amount += amount_diff
        await product.save()
        return product

    async def reserve_products(self, quantities: dict[UUID, int]):
        """Reserve product quantities.

        :param quantities: A dictionary in which the keys are the ``Product`` identifiers and the values are the number
            of units to be reserved.
        :return: ``True`` if all products can be satisfied or ``False`` otherwise.
        """
        feasible = True
        async for product in Product.get(uuids=list(quantities.keys())):
            inventory = product.inventory
            if feasible and inventory.amount < quantities[product.uuid]:
                feasible = False
            inventory.amount -= quantities[product.uuid]
            await product.save()

        if not feasible:
            await self.reserve_products({k: -v for k, v in quantities.items()})
            raise ValueError("The reservation query could not be satisfied.")
