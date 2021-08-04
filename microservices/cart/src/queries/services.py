"""
Copyright (C) 2021 Clariteia SL
This file is part of minos framework.
Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import (
    NoReturn,
)

from dependency_injector.wiring import (
    Provide,
)
from minos.common import (
    AggregateDiff,
)
from minos.cqrs import (
    QueryService,
)
from minos.networks import (
    Request,
    Response,
    enroute,
)
from src.queries.repositories import (
    CartRepository,
)


class CartQueryService(QueryService):
    """Cart Query Service class"""

    repository: CartRepository = Provide["cart_repository"]

    @enroute.rest.query("/carts/{uuid}", "GET")
    @enroute.broker.query("GetCart")
    async def get_cart_items(self, request: Request) -> Response:
        """Get cart items.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()

        res = await self.repository.get_cart_items(content["uuid"])

        return Response(str(res))

    @enroute.broker.event("CartCreated")
    async def cart_or_cart_item_created(self, request: Request) -> NoReturn:
        """Handle the payment create events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

        cart_uuid = diff.uuid

        if len(diff.fields_diff.fields["products"].value) > 0:
            """CartItem Creation"""
            quantity = diff.fields_diff.fields["products"].value[-1].fields["quantity"].value
            product = diff.fields_diff.fields["products"].value[-1].fields["product"]

            item_uuid = str(product.value.fields["uuid"].value)
            item_title = product.value.fields["title"].value
            item_description = product.value.fields["description"].value
            item_price = product.value.fields["price"].value

            await self.repository.insert_or_update_cart_item(
                cart_uuid, item_uuid, quantity, item_title, item_description, item_price
            )
        else:
            """Cart creation"""
            user = diff.fields_diff.fields["user"].value
            await self.repository.create_cart(cart_uuid, user)

    @enroute.broker.event("CartUpdated")
    async def cart_or_cart_item_updated(self, request: Request) -> NoReturn:
        """Handle the payment create events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

        if len(diff.fields_diff.fields["products"].value) > 0:
            """Cart or CartItem update"""
            quantity = diff.fields_diff.fields["products"].value[-1].fields["quantity"].value
            product = diff.fields_diff.fields["products"].value[-1].fields["product"]
            cart_uuid = str(diff.uuid)

            item_uuid = str(product.value.fields["uuid"].value)
            item_title = product.value.fields["title"].value
            item_description = product.value.fields["description"].value
            item_price = product.value.fields["price"].value

            await self.repository.insert_or_update_cart_item(
                cart_uuid, item_uuid, quantity, item_title, item_description, item_price
            )
        else:
            """Cart creation or update"""
            pass

    @enroute.broker.event("CartItemCreated")
    @enroute.broker.event("CartItemUpdated")
    async def cart_item_created_or_updated(self, request: Request) -> NoReturn:
        """Handle the payment create events.
        TODO: Never invoked.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

    @enroute.broker.event("ProductUpdated")
    async def product_updated(self, request: Request) -> NoReturn:
        """Handle the payment create events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

    @enroute.broker.event("CartDeleted")
    async def cart_deleted(self, request: Request) -> NoReturn:
        """Handle the payment delete events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

        if len(diff.fields_diff.fields["products"].value) == 0:
            """Cart creation or update"""
            product = diff.fields_diff.fields["products"].value[-1].fields["product"]
            cart_uuid = str(diff.uuid)

            item_uuid = str(product.value.fields["uuid"].value)

            await self.repository.delete_cart_item(cart_uuid, item_uuid)
        else:
            """Cart Item Creation or update"""
