"""
Copyright (C) 2021 Clariteia SL
This file is part of minos framework.
Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import (
    UUID,
)

from minos.common import (
    ModelType,
)
from minos.cqrs import (
    CommandService,
)
from minos.networks import (
    Request,
    Response,
    enroute,
)
from minos.saga import (
    SagaContext,
)

from ..aggregates import (
    Cart,
    CartItem,
)


class CartCommandService(CommandService):
    """Cart Command Service class"""

    @staticmethod
    @enroute.rest.command("/carts", "POST")
    @enroute.broker.command("CreateCart")
    async def create_cart(request: Request) -> Response:
        """Create a new cart.
        :param request: A request instance containing the information to build a payment instance.
        :return: A response containing the newly created payment instance.
        """
        content = await request.content()
        user = content["user"]
        cart = await Cart.create(user=user, products=[])

        return Response(cart)

    @enroute.rest.command("/carts/{uuid}/items", "POST")
    @enroute.broker.command("CreateCartItem")
    async def add_cart_item(self, request: Request) -> Response:
        """Create cart item.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()
        cart = content["uuid"]
        product_uuid = content["product_uuid"]
        quantity = content["quantity"]
        await self.saga_manager.run(
            "AddCartItem", context=SagaContext(cart_id=cart, product_uuid=product_uuid, quantity=quantity)
        )

        return Response({})

    @enroute.rest.command("/carts/{uuid}/items", "DELETE")
    @enroute.broker.command("RemoveCartItem")
    async def remove_cart_item(self, request: Request) -> Response:
        """Create cart item.
        TODO: Correctly remove Cart Item
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()
        cart = content["uuid"]
        product = content["product_uuid"]

        idx, product = await self._get_cart_item(cart, product)

        await self.saga_manager.run(
            "RemoveCartItem", context=SagaContext(cart_id=cart, product_uuid=product, idx=idx, product=product)
        )

        return Response({})

    @staticmethod
    @enroute.rest.command("/carts/{uuid}", "GET")
    @enroute.broker.command("GetCart")
    async def get_cart(request: Request) -> Response:
        """Get cart items.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()
        cart = await Cart.get_one(content["uuid"])

        return Response(cart)

    @staticmethod
    @enroute.rest.command("/carts/{uuid}", "DELETE")
    @enroute.broker.command("DeleteCart")
    async def delete_cart(request: Request) -> Response:
        """Delete cart.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()
        cart = await Cart.get_one(content["uuid"])
        result = await cart.delete()

        return Response(result)

    @staticmethod
    async def _get_cart_item(cart_id: UUID, product_uuid: UUID):
        cart = await Cart.get_one(cart_id)
        for idx, product in enumerate(cart.products):
            if str(product.product) == product_uuid:
                return idx, product
