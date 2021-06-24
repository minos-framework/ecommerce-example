"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""

from minos.common import (
    Service,
)

from .aggregates import (
    Inventory,
)


class InventoryService(Service):
    """Inventory Service class"""

    @staticmethod
    async def create_inventory(product: int, amount: int) -> Inventory:
        """Create an inventory.

        :param product: TODO.
        :param amount: int
        :return: TODO.
        """
        return await Inventory.create(product, amount)

    @staticmethod
    async def get_inventories(ids: list[int]) -> list[Inventory]:
        """Get a list of inventories.

        :param ids: List of inventory identifiers.
        :return: A list of ``Inventory`` instances.
        """
        values = {v.id: v async for v in Inventory.get(ids=ids)}
        return [values[id] for id in ids]
