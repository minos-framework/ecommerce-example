"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import (
    NoReturn,
)
from uuid import (
    UUID,
)

from dependency_injector.wiring import (
    Provide,
)
from minos.common import (
    UUID_REGEX,
    AggregateDiff,
    ModelType,
)
from minos.cqrs import (
    QueryService,
)
from minos.networks import (
    Request,
    Response,
    ResponseException,
    enroute,
)

from .repositories import (
    ReviewQueryRepository,
)


class ReviewQueryService(QueryService):
    """Product Query Service class."""

    repository: ReviewQueryRepository = Provide["review_repository"]

    @enroute.rest.query("/reviews/product/{uuid}", "GET")
    @enroute.broker.query("GetProductReviews")
    async def get_product_reviews(self, request: Request) -> Response:
        """Get cart items.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()

        res = await self.repository.find_by_product(content["uuid"])

        return Response(res)

    @enroute.rest.query("/reviews/user/{uuid}", "GET")
    @enroute.broker.query("GetUserReviews")
    async def get_user_reviews(self, request: Request) -> Response:
        """Get cart items.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()

        res = await self.repository.find_by_user(content["uuid"])

        return Response(res)

    @enroute.rest.query("/reviews/product/{uuid}/top", "GET")
    @enroute.broker.query("GetTopProductRating")
    async def get_top_product_rating(self, request: Request) -> Response:
        """Get cart items.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()

        res = await self.repository.top_product_rating(content["uuid"])

        return Response(res)

    @enroute.rest.query("/reviews/product/{uuid}/worst", "GET")
    @enroute.broker.query("GetWorstProductRating")
    async def get_worst_product_rating(self, request: Request) -> Response:
        """Get cart items.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()

        res = await self.repository.worst_product_rating(content["uuid"])

        return Response(res)

    @enroute.rest.query("/reviews/top_rated_products", "GET")
    @enroute.broker.query("GetTopRatedProducts")
    async def get_top_rated_products(self, request: Request) -> Response:
        """Get cart items.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()

        res = await self.repository.top_rated_products()

        return Response(res)

    @enroute.rest.query("/reviews/worst_rated_products", "GET")
    @enroute.broker.query("GetWorstRatedProducts")
    async def get_worst_rated_products(self, request: Request) -> Response:
        """Get cart items.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()

        res = await self.repository.worst_rated_products()

        return Response(res)

    @enroute.broker.event("ReviewCreated")
    async def review_created(self, request: Request) -> NoReturn:
        """Handle the product create and update events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        await self.repository.create(uuid=diff.uuid, version=diff.version, **diff.fields_diff)

    @enroute.broker.event("ReviewUpdated")
    async def review_created(self, request: Request) -> NoReturn:
        """Handle the product create and update events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        await self.repository.update(uuid=diff.uuid, version=diff.version, **diff.fields_diff)

    @enroute.broker.event("ProductUpdated.title")
    async def product_title_updated(self, request: Request) -> NoReturn:
        """Handle the product create and update events.
        TODO: Uncomplete
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        print(diff)

    @enroute.broker.event("UserUpdated.username")
    async def username_updated(self, request: Request) -> NoReturn:
        """Handle the product create and update events.
        TODO: Uncomplete
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        print(diff)
