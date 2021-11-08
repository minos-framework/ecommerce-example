from __future__ import (
    annotations,
)

from asyncio import (
    gather,
)
from uuid import (
    UUID,
)

from minos.aggregate import (
    Aggregate,
    ValueObject,
)


class Product(Aggregate):
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

    @classmethod
    async def reserve(cls, quantities: dict[UUID, int]) -> None:
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
            await cls.reserve({k: -v for k, v in quantities.items()})
            raise ValueError("The reservation query could not be satisfied.")

    @classmethod
    async def purchase(cls, quantities: dict[UUID, int]) -> None:
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
            await cls.purchase({k: -v for k, v in quantities.items()})
            raise ValueError("The purchase products query could not be satisfied.")


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
