"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import (
    UUID,
)

from minos.common import (
    Service,
)
from minos.saga import (
    SagaContext,
)

from .aggregates import (
    Cart,
    CartItem,
)


class CartService(Service):
    """Cart Service class"""

    @staticmethod
    async def create_cart(user: int) -> Cart:
        """
        Creates a cart

        :param user: The user ID.
        """
        cart = await Cart.create(user=user, products=[])

        return cart

    async def add_item(self, cart: int, product: int, quantity: int) -> UUID:
        """
        Add product to the Cart

        :param cart: Cart ID.
        :param product: The product identifiers to be included in the cart.
        :param quantity: Product quantity.
        """
        return await self.saga_manager.run(
            "AddCartItem", context=SagaContext(cart_id=cart, product_id=product, quantity=quantity)
        )

    async def delete_item(self, cart: int, product: int) -> UUID:
        """
        Remove product from Cart

        :param cart: Cart ID.
        :param product: The product identifiers to be included in the cart.
        """

        idx, product = self._get_cart_item(cart, product)

        return await self.saga_manager.run(
            "RemoveCartItem", context=SagaContext(cart_id=cart, product_id=product, idx=idx, product=product)
        )

    @staticmethod
    async def update_item(user_id: int, product: CartItem) -> CartItem:
        pass

    @staticmethod
    async def get_cart(user: int) -> Cart:
        pass

    @staticmethod
    async def delete_cart(user_id: int, cart: Cart):
        pass

    @staticmethod
    async def _get_cart_item(cart_id: int, product_id: int):
        cart = await Cart.get_one(cart_id)
        for idx, product in enumerate(cart.products):
            if product.id == product_id:
                return idx, product
