"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from __future__ import (
    annotations,
)

from typing import (
    NoReturn,
)

from minos.common import (
    Aggregate,
    ValueObject,
)


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


class Product(Aggregate):
    """Product class."""

    code: str
    title: str
    description: str
    price: float

    inventory: Inventory

    def set_inventory_amount(self, amount: int) -> NoReturn:
        """Update the inventory amount.

        :param amount: The new inventory amount.
        :return: This method does not return anything.
        """
        self.inventory = self.inventory.set_amount(amount)

    def update_inventory_amount(self, amount_diff: int) -> NoReturn:
        """Update the inventory amount.

        :param amount_diff: The difference from the actual amount.
        :return: This method does not return anything.
        """
        self.inventory = self.inventory.update_amount(amount_diff)
