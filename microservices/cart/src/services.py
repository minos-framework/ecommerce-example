"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import uuid4
from minos.common import Service
from minos.saga import SagaContext
from .aggregates import Cart


class CartService(Service):
    """Cart Service class"""

    async def add_items(self, user_id: int, products: list[int]) -> Cart:
        """
        Creates a cart

        :param user_id: The user ID.
        :param products: The list of product identifiers to be included in the ticket.
        """
        code = uuid4().hex.upper()[0:6]
        cart = await Cart.create(code, user_id, products)
        await self.saga_manager.run("CreateCart", context=SagaContext(cart=cart, product_ids=products))

        return cart
