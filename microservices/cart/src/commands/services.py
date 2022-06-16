from minos.cqrs import (
    CommandService,
)
from minos.networks import (
    HttpRequest,
    Request,
    Response,
    enroute,
)


class CartCommandService(CommandService):
    """Cart Command Service class"""

    @enroute.rest.command("/carts", "POST")
    @enroute.broker.command("CreateCart")
    async def create_cart(self, request: Request) -> Response:
        """Create a new cart.
        :param request: A request instance containing the information to build a payment instance.
        :return: A response containing the newly created payment instance.
        """
        content = await request.content()
        user = content["user"]
        cart = await self.aggregate.create_cart(user)
        return Response(cart)

    @enroute.rest.command("/carts/{uuid}/items", "POST")
    @enroute.broker.command("CreateCartItem")
    async def add_cart_item(self, request: Request) -> Response:
        """Create cart item.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()

        if isinstance(request, HttpRequest):
            params = await request.params()
            cart = params["uuid"]
        else:
            cart = content["uuid"]

        product_uuid = content["product_uuid"]
        quantity = content["quantity"]
        execution_uuid = await self.aggregate.add_cart_item(cart, product_uuid, quantity)

        return Response(execution_uuid)

    @enroute.rest.command("/carts/{uuid}/items", "PUT")
    @enroute.broker.command("UpdateCartItem")
    async def update_cart_item(self, request: Request) -> Response:
        """Create cart item.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()

        if isinstance(request, HttpRequest):
            params = await request.params()
            cart = params["uuid"]
        else:
            cart = content["uuid"]

        product_uuid = content["product_uuid"]
        quantity = content["quantity"]
        execution_uuid = await self.aggregate.update_cart_item(cart, product_uuid, quantity)
        return Response(execution_uuid)

    @enroute.rest.command("/carts/{uuid}/items", "DELETE")
    @enroute.broker.command("RemoveCartItem")
    async def remove_cart_item(self, request: Request) -> Response:
        """Create cart item.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()

        if isinstance(request, HttpRequest):
            params = await request.params()
            cart = params["uuid"]
        else:
            cart = content["uuid"]

        product_uuid = content["product_uuid"]

        execution_uuid = await self.aggregate.remove_cart_item(cart, product_uuid)

        return Response(execution_uuid)

    @enroute.rest.command("/carts/{uuid}", "DELETE")
    @enroute.broker.command("DeleteCart")
    async def delete_cart(self, request: Request) -> Response:
        """Delete cart.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        if isinstance(request, HttpRequest):
            params = await request.params()
            uuid = params["uuid"]
        else:
            content = await request.content()
            uuid = content["uuid"]

        execution_uuid = await self.aggregate.delete_cart(uuid)

        return Response(execution_uuid)
