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
    enroute,
)
from src.queries.repositories import (
    CartRepository,
)


class CartQueryService(QueryService):
    """Cart Query Service class"""

    repository: CartRepository = Provide["cart_repository"]

    @enroute.broker.event("CartCreated")
    @enroute.broker.event("CartUpdated")
    async def cart_created_or_updated(self, request: Request) -> NoReturn:
        """Handle the payment create events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

        quantity = diff.fields_diff.fields["products"].value[0].fields['quantity'].value
        product = diff.fields_diff.fields["products"].value[0].fields['product']
        cart_uuid = str(diff.uuid)

        item_uuid = str(product.value.fields["uuid"].value)
        item_title = product.value.fields["title"].value
        item_description = product.value.fields["description"].value
        item_price = product.value.fields["price"].value

        await self.repository.insert_or_update_cart_item(cart_uuid, item_uuid, quantity, item_title, item_description,
                                                         item_price)

    @enroute.broker.event("CartItemCreated")
    @enroute.broker.event("CartItemUpdated")
    async def cart_item_created_or_updated(self, request: Request) -> NoReturn:
        """Handle the payment create events.
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
        """
        await self.repository.delete(diff.uuid)
        """
