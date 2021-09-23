from dependency_injector.wiring import Provide
from minos.common import AggregateDiff
from minos.cqrs import QueryService
from minos.networks import (
    Request,
    Response,
    enroute,
)

from .repositories import ReviewQueryRepository


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

        res = await self.repository.get_reviews_by_product(content["uuid"])

        return Response(res)

    @enroute.rest.query("/reviews/user/{uuid}", "GET")
    @enroute.broker.query("GetCustomerReviews")
    async def get_user_reviews(self, request: Request) -> Response:
        """Get cart items.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()

        res = await self.repository.get_reviews_by_user(content["uuid"])

        return Response(res)

    @enroute.rest.query("/reviews/product/{uuid}/score", "GET")
    @enroute.broker.query("GetTopProductRating")
    async def get_product_score_reviews(self, request: Request) -> Response:
        """Get cart items.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()

        order = "asc"
        if "order" in content:
            order = content["order"]

        limit = 1
        if "limit" in content:
            limit = content["limit"]

        res = await self.repository.product_score(content["uuid"], limit, order)

        return Response(res)

    @enroute.rest.query("/reviews/score", "GET")
    @enroute.broker.query("GetTopRatedProducts")
    async def get_reviews_score(self, request: Request) -> Response:
        """Get cart items.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()

        order = "asc"
        if "order" in content:
            order = content["order"]

        limit = 1
        if "limit" in content:
            limit = content["limit"]

        res = await self.repository.reviews_score(limit, order)

        return Response(res)

    @enroute.rest.query("/reviews/last", "GET")
    @enroute.broker.query("GetLastReviews")
    async def get_last_reviews(self, request: Request) -> Response:
        """Get cart items.
        :param request: A request instance containing the payment identifiers.
        :return: A response containing the queried payment instances.
        """
        content = await request.content()

        limit = 1
        if "limit" in content:
            limit = content["limit"]

        res = await self.repository.last_reviews(limit)

        return Response(res)

    @enroute.broker.event("ReviewCreated")
    async def review_created(self, request: Request) -> None:
        """Handle the product create and update events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        await self.repository.create(uuid=diff.uuid, version=diff.version, **diff.fields_diff)

    @enroute.broker.event("ReviewUpdated")
    async def review_updated(self, request: Request) -> None:
        """Handle the product create and update events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        await self.repository.update(uuid=diff.uuid, version=diff.version, **diff.fields_diff)

    @enroute.broker.event("ProductUpdated.title")
    async def product_title_updated(self, request: Request) -> None:
        """Handle the product create and update events.
        TODO: Uncomplete
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        print(diff)

    @enroute.broker.event("CustomerUpdated.username")
    async def username_updated(self, request: Request) -> None:
        """Handle the product create and update events.
        TODO: Uncomplete
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        print(diff)
