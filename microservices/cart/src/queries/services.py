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

        return Response(res)

    @enroute.broker.event("CartCreated")
    async def cart_created(self, request: Request) -> NoReturn:
        """Handle the payment create events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

        await self.repository.create_cart(diff.uuid, diff.version, diff.user)

    @enroute.broker.event("CartUpdated")
    async def cart_updated(self, request: Request) -> NoReturn:
        """Handle the payment create events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        print(diff)

    @enroute.broker.event("CartUpdated.entries.create")
    async def cart_item_created(self, request: Request) -> NoReturn:
        """Handle the payment create events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

        products = diff["entries"]

        await self.repository.insert_cart_item(
            diff.uuid,
            products.product.uuid,
            products.quantity,
            products.product.title,
            products.product.description,
            products.product.price,
        )

    @enroute.broker.event("CartUpdated.entries.delete")
    async def cart_item_deleted(self, request: Request) -> NoReturn:
        """Handle the payment create events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

        products = diff["entries"]

        await self.repository.delete_cart_item(diff.uuid, products.product.uuid)

    @enroute.broker.event("CartUpdated.entries.update")
    async def cart_item_updated(self, request: Request) -> NoReturn:
        """Handle the payment create events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        products = diff["entries"]

        await self.repository.update_cart_item(
            diff.uuid,
            products.product.uuid,
            products.quantity,
            products.product.title,
            products.product.description,
            products.product.price,
        )

    @enroute.broker.event("ProductUpdated.price")
    @enroute.broker.event("ProductUpdated.title")
    @enroute.broker.event("ProductUpdated.description")
    async def product_updated(self, request: Request) -> NoReturn:
        """Handle the payment create events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        await self.repository.update_cart_items(uuid=diff.uuid, **diff.fields_diff)
        print(diff)

    @enroute.broker.event("CartDeleted")
    async def cart_deleted(self, request: Request) -> NoReturn:
        """Handle the payment delete events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        cart_uuid = diff.uuid

        await self.repository.delete_cart(cart_uuid)
