from __future__ import (
    annotations,
)

from asyncio import (
    gather,
)
from typing import (
    Any,
    Optional,
)
from uuid import (
    UUID,
    uuid4,
)

from minos.aggregate import (
    Aggregate,
    RootEntity,
    ValueObject,
)
from minos.networks import (
    BrokerMessageV1,
    BrokerMessageV1Payload,
)


class Product(RootEntity):
    """Product class."""

    code: str
    title: str
    description: str
    price: float

    inventory: Inventory

    def set_inventory_amount(self, amount: int) -> None:
        """Update the inventory amount.

        :param amount: The new inventory amount.
        :return: This method does not return anything.
        """
        self.inventory = self.inventory.set_amount(amount)

    def update_inventory_amount(self, amount_diff: int) -> None:
        """Update the inventory amount.

        :param amount_diff: The difference from the actual amount.
        :return: This method does not return anything.
        """
        self.inventory = self.inventory.update_amount(amount_diff)


class Inventory(ValueObject):
    """Inventory Object Value class."""

    amount: int
    reserved: int
    sold: int

    @staticmethod
    def empty() -> Inventory:
        """Create an empty inventory.

        :return: An ``Inventory`` instance.
        """
        return Inventory(amount=0, reserved=0, sold=0)

    def set_amount(self, amount: int) -> Inventory:
        """Create a new inventory with updated amount.

        :param amount: The new inventory amount.
        :return: An ``Inventory`` instance.
        """
        return Inventory(amount, self.reserved, self.sold)

    def update_amount(self, amount_diff: int) -> Inventory:
        """Create a new inventory with updated amount.

        :param amount_diff: The difference from the actual amount.
        :return: An ``Inventory`` instance.
        """
        return Inventory(self.amount + amount_diff, self.reserved, self.sold)


class ProductAggregate(Aggregate[Product]):
    """Product Aggregate class."""

    async def something(self):
        message = BrokerMessageV1("bar", BrokerMessageV1Payload("foo"),)
        await self.broker_publisher.send(message)

    @staticmethod
    async def create_product(title: str, description: str, price: float) -> Product:
        """TODO"""
        code = uuid4().hex.upper()[0:6]
        inventory = Inventory.empty()

        product = await Product.create(code, title, description, price, inventory)
        return product

    @staticmethod
    async def update_inventory(uuid: UUID, amount: int) -> Product:
        """TODO"""
        product = await Product.get(uuid)
        product.set_inventory_amount(amount)
        await product.save()
        return product

    @staticmethod
    async def update_inventory_diff(uuid: UUID, amount_diff: int) -> Product:
        """TODO"""
        product = await Product.get(uuid)
        product.update_inventory_amount(amount_diff)
        await product.save()
        return product

    @staticmethod
    async def check_positive_inventory(uuid: UUID, amount: Optional[int], amount_diff: Optional[int]) -> bool:
        """TODO"""
        if amount_diff is not None:
            product = await Product.get(uuid)
            amount = product.inventory.amount + amount_diff

        return amount >= 0

    @staticmethod
    async def update_product(uuid: UUID, title: str, description: str, price: float) -> Product:
        """TODO"""

        product = await Product.get(uuid)
        product.title = title
        product.description = description
        product.price = price

        await product.save()
        return product

    @staticmethod
    async def update_product_diff(uuid: UUID, content: dict[str, Any]) -> Product:
        """TODO"""

        product = await Product.get(uuid)

        if "title" in content:
            product.title = content["title"]

        if "description" in content:
            product.description = content["description"]

        if "price" in content:
            product.price = content["price"]

        await product.save()
        return product

    @staticmethod
    async def delete_product(uuid: UUID) -> None:
        """TODO"""
        product = await Product.get(uuid)
        await product.delete()

    async def reserve(self, quantities: dict[UUID, int]) -> None:
        """Reserve product quantities.

        :param quantities: A dictionary in which the keys are the ``Product`` identifiers and the values are
        the number
            of units to be reserved.
        :return: ``True`` if all products can be satisfied or ``False`` otherwise.
        """
        feasible = True
        products = await gather(*(Product.get(uuid) for uuid in quantities.keys()))
        for product in products:
            inventory = product.inventory
            reserved = inventory.reserved
            if feasible and (inventory.amount - reserved) < quantities[product.uuid]:
                feasible = False
            reserved += quantities[product.uuid]
            product.inventory = Inventory(inventory.amount, reserved, inventory.sold)
            await product.save()

        if not feasible:
            await self.reserve({k: -v for k, v in quantities.items()})
            raise ValueError("The reservation query could not be satisfied.")

    async def purchase(self, quantities: dict[UUID, int]) -> None:
        """Purchase products.

        :param quantities: A dictionary in which the keys are the ``Product`` identifiers and the values are
        the number
            of units to be reserved.
        :return: ``True`` if all products can be satisfied or ``False`` otherwise.
        """
        feasible = True
        products = await gather(*(Product.get(uuid) for uuid in quantities.keys()))
        for product in products:
            inventory = product.inventory
            reserved = inventory.reserved
            sold = inventory.sold
            amount = inventory.amount - quantities[product.uuid]
            if feasible and amount <= quantities[product.uuid]:
                feasible = False
            reserved -= quantities[product.uuid]
            sold += quantities[product.uuid]
            product.inventory = Inventory(amount, reserved, sold)
            await product.save()

        if not feasible:
            await self.purchase({k: -v for k, v in quantities.items()})
            raise ValueError("The purchase products query could not be satisfied.")
