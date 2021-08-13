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
    ProductQueryRepository,
)


class ProductQueryService(QueryService):
    """Product Query Service class."""

    repository: ProductQueryRepository = Provide["product_repository"]

    @staticmethod
    @enroute.broker.query("GetProducts")
    @enroute.rest.query("/products", "GET")
    async def get_products(request: Request) -> Response:
        """Get products.

        :param request: The ``Request`` instance that contains the product identifiers.
        :return: A ``Response`` instance containing the requested products.
        """
        try:
            content = await request.content(model_type=ModelType.build("Query", {"uuids": list[UUID]}))
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        try:
            from ..aggregates import (
                Product,
            )

            iterable = Product.get(uuids=content["uuids"])
            values = {v.uuid: v async for v in iterable}
            products = [values[uuid] for uuid in content["uuids"]]
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting products: {exc!r}")

        return Response(products)

    @staticmethod
    @enroute.broker.query("GetProduct")
    @enroute.rest.query(f"/products/{{uuid:{UUID_REGEX.pattern}}}", "GET")
    async def get_product(request: Request) -> Response:
        """Get product.

        :param request: The ``Request`` instance that contains the product identifier.
        :return: A ``Response`` instance containing the requested product.
        """
        try:
            content = await request.content(model_type=ModelType.build("Query", {"uuid": UUID}))
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        try:
            from ..aggregates import (
                Product,
            )

            product = await Product.get_one(content["uuid"])
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting the product: {exc!r}")

        return Response(product)

    @staticmethod
    @enroute.broker.query("GetProducts")
    @enroute.rest.query("/products", "GET")
    async def get_products(request: Request) -> Response:
        """Get products.
        :param request: The ``Request`` instance that contains the product identifiers.
        :return: A ``Response`` instance containing the requested products.
        """
        try:
            content = await request.content(model_type=ModelType.build("Query", {"uuids": list[UUID]}))
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        try:
            from ..aggregates import (
                Product,
            )

            iterable = Product.get(uuids=content["uuids"])
            values = {v.uuid: v async for v in iterable}
            products = [values[uuid] for uuid in content["uuids"]]
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting products: {exc!r}")

        return Response(products)

    @staticmethod
    @enroute.broker.query("GetProduct")
    @enroute.rest.query(f"/products/{{uuid:{UUID_REGEX.pattern}}}", "GET")
    async def get_product(request: Request) -> Response:
        """Get product.
        :param request: The ``Request`` instance that contains the product identifier.
        :return: A ``Response`` instance containing the requested product.
        """
        try:
            content = await request.content(model_type=ModelType.build("Query", {"uuid": UUID}))
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        try:
            from ..aggregates import (
                Product,
            )

            product = await Product.get_one(content["uuid"])
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting the product: {exc!r}")

        return Response(product)

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
    async def product_created(self, request: Request) -> NoReturn:
        """Handle the product create and update events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        # await self.repository.create(uuid=diff.uuid, version=diff.version, **diff.differences.differences)
        print(diff)

    @enroute.broker.event("ProductUpdated")
    async def product_updated(self, request: Request) -> NoReturn:
        """Handle the product create and update events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        # await self.repository.update(uuid=diff.uuid, version=diff.version, **diff.fields_diff.avro_data)
        print(diff)

    @enroute.broker.event("ProductUpdated.description")
    async def product_updated_description(self, request: Request) -> NoReturn:
        """Handle the product create and update events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        print(diff)

    @enroute.broker.event("ProductUpdated.reviews.create")
    async def product_updated_reviews_create(self, request: Request) -> NoReturn:
        """Handle the product create and update events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        print("reviews.create", diff.differences)

    @enroute.broker.event("ProductDeleted")
    async def product_deleted(self, request: Request) -> NoReturn:
        """Handle the product delete events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        await self.repository.delete(diff.uuid)
