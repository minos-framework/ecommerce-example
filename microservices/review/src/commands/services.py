from minos.cqrs import (
    CommandService,
)
from minos.networks import (
    HttpRequest,
    Request,
    Response,
    enroute,
)


class ReviewCommandService(CommandService):
    """Product Service class"""

    @enroute.broker.command("CreateReview")
    @enroute.rest.command("/reviews", "POST")
    async def create_review(self, request: Request) -> Response:
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

        product = await self.aggregate.create_review(
            product=product, user=user, title=title, description=description, score=score
        )

        return Response(product)

    @enroute.broker.command("UpdateReview")
    @enroute.rest.command("/reviews/{uuid}", "PUT")
    async def update_review(self, request: Request) -> Response:
        """Create a new product instance.

        :param request: The ``Request`` that contains the needed information to create the product.
        :return: A ``Response`` containing the already created product.
        """
        content = await request.content()
        if isinstance(request, HttpRequest):
            params = await request.params()
            uuid = params["uuid"]
        else:
            uuid = content["uuid"]

        review = await self.aggregate.update_review(uuid, content)

        return Response(review)
