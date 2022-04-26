from __future__ import (
    annotations,
)

from typing import (
    Optional,
)
from uuid import (
    UUID,
)

from minos.aggregate import (
    Aggregate,
    Entity,
    EntitySet,
    ExternalEntity,
    Ref,
    RootEntity,
)
from minos.saga import (
    SagaContext,
)


class Cart(RootEntity):
    """Cart RootEntity class."""

    user: int
    entries: EntitySet[CartEntry]


class CartEntry(Entity):
    """Cart Item DeclarativeModel class."""

    quantity: int
    product: Ref[Product]


class Product(ExternalEntity):
    """Product ExternalEntity class."""

    title: str
    description: str
    price: float


class CartAggregate(Aggregate[Cart]):
    """Cart Aggregate class."""

    async def create_cart(self, user: int) -> Cart:
        """TODO"""
        cart, _ = await self.repository.create(Cart, user=user, entries=EntitySet())
        return cart

    async def add_cart_item(self, cart_uuid: UUID, product_uuid: UUID, quantity: int) -> UUID:
        """TODO"""

        from .commands import (
            ADD_CART_ITEM,
        )

        saga_execution = await self.saga_manager.run(
            ADD_CART_ITEM, context=SagaContext(cart_id=cart_uuid, product_uuid=product_uuid, quantity=quantity)
        )
        return saga_execution.uuid

    async def update_cart_item(self, cart_uuid: UUID, product_uuid: UUID, quantity: int) -> UUID:
        """TODO"""
        from .commands import (
            UPDATE_CART_ITEM,
        )

        saga_execution = await self.saga_manager.run(
            UPDATE_CART_ITEM, context=SagaContext(cart_id=cart_uuid, product_uuid=product_uuid, quantity=quantity)
        )
        return saga_execution.uuid

    async def remove_cart_item(self, cart_uuid: UUID, product_uuid: UUID) -> UUID:
        """TODO"""
        from .commands import (
            REMOVE_CART_ITEM,
        )

        idx, product = await self._get_cart_item(cart_uuid, product_uuid)

        saga_execution = await self.saga_manager.run(
            REMOVE_CART_ITEM, context=SagaContext(cart_id=cart_uuid, product_uuid=product_uuid, product=product)
        )
        return saga_execution.uuid

    async def delete_cart(self, uuid: UUID) -> UUID:
        """TODO"""
        from .commands import (
            DELETE_CART,
        )

        cart = await self.repository.get(Cart, uuid)

        saga_execution = await self.saga_manager.run(DELETE_CART, context=SagaContext(cart=cart))
        return saga_execution.uuid

    async def _get_cart_item(self, cart_id: UUID, product_uuid: UUID) -> Optional[tuple[int, CartEntry]]:
        cart = await self.repository.get(Cart, cart_id)
        for idx, product in enumerate(cart.entries):
            if str(product.product) == product_uuid:
                return idx, product
