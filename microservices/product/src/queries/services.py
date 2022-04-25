from minos.aggregate import (
    Event,
)
from minos.common import (
    UUID_REGEX,
    Inject,
)
from minos.cqrs import (
    QueryService,
)
from minos.networks import (
    HttpRequest,
    Request,
    Response,
    ResponseException,
    enroute,
)

from .repositories import (
    ProductQueryRepository,
)


class ProductQueryService(QueryService):
    """Product Query Service class."""

    @Inject()
    def __init__(self, repository: ProductQueryRepository, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = repository

    @enroute.rest.query("/products", "GET")
    async def get_all_products(self, request: Request) -> Response:
        """Get all products.

        :param request: The ``Request`` instance that contains the product identifiers.
        :return: A ``Response`` instance containing the requested products.
        """

        res = await self.repository.get_all()

        return Response(res)

    @enroute.rest.query(f"/products/{{uuid:{UUID_REGEX.pattern}}}", "GET")
    async def get_product_by_uuid(self, request: HttpRequest) -> Response:
        """Get all products.

        :param request: The ``Request`` instance that contains the product identifiers.
        :return: A ``Response`` instance containing the requested products.
        """
        params = await request.params()
        uuid = params["uuid"]
        res = await self.repository.get(uuid)

        return Response(res)

    # noinspection PyUnusedLocal
    @enroute.rest.query("/products/without-stock", "GET")
    @enroute.broker.query("GetProductsWithoutStock")
    async def get_products_without_stock(self, request: Request) -> Response:
        """Get the products without stock.

        :param request: A request without any content.
        :return: A response containing the products without stock.
        """
        uuids = await self.repository.get_without_stock()
        return Response(uuids)

    @enroute.broker.query("GetMostSoldProducts")
    def get_most_sold_products(self, request: Request) -> Response:
        """Get the most sold products.

        :param request: A request containing the maximum number of products to be retrieved.
        :return: A response containing the most sold products.
        """
        raise ResponseException("Not Implemented yet!")

    @enroute.broker.event("ProductCreated")
    async def product_created(self, request: Request) -> None:
        """Handle the product create and update events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: Event = await request.content()
        await self.repository.create(uuid=diff.uuid, version=diff.version, **diff.fields_diff)

    @enroute.broker.event("ProductUpdated")
    async def product_updated(self, request: Request) -> None:
        """Handle the product create and update events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: Event = await request.content()
        await self.repository.update(uuid=diff.uuid, version=diff.version, **diff.fields_diff)

    @enroute.broker.event("ProductDeleted")
    async def product_deleted(self, request: Request) -> None:
        """Handle the product delete events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: Event = await request.content()
        await self.repository.delete(diff.uuid)

    @enroute.broker.event("ReviewCreated")
    async def review_created(self, request: Request) -> None:
        """Handle review created or updated events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: Event = await request.content()
        await self.repository.update(uuid=diff.uuid, version=diff.version, **diff.fields_diff)

    @enroute.broker.event("ReviewUpdated.score")
    async def review_updated(self, request: Request) -> None:
        """Handle review created or updated events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: Event = await request.content()
        await self.repository.update(uuid=diff.uuid, version=diff.version, **diff.fields_diff)
