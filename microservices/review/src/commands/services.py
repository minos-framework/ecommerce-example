"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.cqrs import (
    CommandService,
)
from minos.networks import (
    Request,
    Response,
    enroute,
)

from ..aggregates import (
    Review,
)


class ReviewCommandService(CommandService):
    """Product Service class"""

    @staticmethod
    @enroute.broker.command("CreateReview")
    @enroute.rest.command("/reviews", "POST")
    async def create_review(request: Request) -> Response:
        """Create a new product instance.

        :param request: The ``Request`` that contains the needed information to create the product.
        :return: A ``Response`` containing the already created product.
        """
        content = await request.content()
        product = content["product"]
        user = content["user"]
        title = content["title"]
        description = content["description"]
        score = content["score"]

        product = await Review.create(product=product, user=user, title=title, description=description, score=score)

        return Response(product)

    @staticmethod
    @enroute.broker.command("UpdateReview")
    @enroute.rest.command("/reviews/{uuid}", "PUT")
    async def update_review(request: Request) -> Response:
        """Create a new product instance.

        :param request: The ``Request`` that contains the needed information to create the product.
        :return: A ``Response`` containing the already created product.
        """
        content = await request.content()
        uuid = content["uuid"]

        review = await Review.get(uuid)

        kwargs = dict(content)
        kwargs.pop("uuid")
        await review.update(**kwargs)

        return Response(review)
