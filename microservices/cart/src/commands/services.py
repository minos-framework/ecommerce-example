from uuid import (
    UUID,
)

from minos.aggregate import (
    EntitySet,
)
from minos.cqrs import (
    CommandService,
)
from minos.networks import (
    Request,
    Response,
    RestRequest,
    enroute,
)
from minos.saga import (
    SagaContext,
)

from ..aggregates import (
    Cart,
)
from .sagas import (
    ADD_CART_ITEM,
    DELETE_CART,
    REMOVE_CART_ITEM,
    UPDATE_CART_ITEM,
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
        cart = await Cart.create(user=user, entries=EntitySet())
        return Response(cart)

    @enroute.rest.command("/carts/{uuid}/items", "POST")
    @enroute.broker.command("CreateCartItem")
    async def add_cart_item(self, request: Request) -> Response:
        """Create cart item.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()

        if isinstance(request, RestRequest):
            params = await request.params()
            cart = params["uuid"]
        else:
            cart = content["uuid"]

        product_uuid = content["product_uuid"]
        quantity = content["quantity"]
        saga_execution = await self.saga_manager.run(
            ADD_CART_ITEM, context=SagaContext(cart_id=cart, product_uuid=product_uuid, quantity=quantity)
        )

        return Response(saga_execution.uuid)

    @enroute.rest.command("/carts/{uuid}/items", "PUT")
    @enroute.broker.command("UpdateCartItem")
    async def update_cart_item(self, request: Request) -> Response:
        """Create cart item.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()

        if isinstance(request, RestRequest):
            params = await request.params()
            cart = params["uuid"]
        else:
            cart = content["uuid"]

        product_uuid = content["product_uuid"]
        quantity = content["quantity"]
        saga_execution = await self.saga_manager.run(
            UPDATE_CART_ITEM, context=SagaContext(cart_id=cart, product_uuid=product_uuid, quantity=quantity)
        )

        return Response(saga_execution.uuid)

    @enroute.rest.command("/carts/{uuid}/items", "DELETE")
    @enroute.broker.command("RemoveCartItem")
    async def remove_cart_item(self, request: Request) -> Response:
        """Create cart item.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()

        if isinstance(request, RestRequest):
            params = await request.params()
            cart = params["uuid"]
        else:
            cart = content["uuid"]

        product_uuid = content["product_uuid"]

        idx, product = await self._get_cart_item(cart, product_uuid)

        saga_execution = await self.saga_manager.run(
            REMOVE_CART_ITEM, context=SagaContext(cart_id=cart, product_uuid=product_uuid, product=product)
        )

        return Response(saga_execution.uuid)

    @enroute.rest.command("/carts/{uuid}", "DELETE")
    @enroute.broker.command("DeleteCart")
    async def delete_cart(self, request: Request) -> Response:
        """Delete cart.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        if isinstance(request, RestRequest):
            params = await request.params()
            uuid = params["uuid"]
        else:
            content = await request.content()
            uuid = content["uuid"]

        cart = await Cart.get(uuid)

        saga_execution = await self.saga_manager.run(DELETE_CART, context=SagaContext(cart=cart))

        return Response(saga_execution.uuid)

    @staticmethod
    async def _get_cart_item(cart_id: UUID, product_uuid: UUID):
        cart = await Cart.get(cart_id)
        for idx, product in enumerate(cart.entries):
            if str(product.product) == product_uuid:
                return idx, product
