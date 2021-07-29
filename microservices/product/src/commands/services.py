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
    uuid4,
)

from minos.common import (
    MinosSnapshotAggregateNotFoundException,
    MinosSnapshotDeletedAggregateException,
    ModelType,
)
from minos.cqrs import (
    CommandService,
)
from minos.networks import (
    Request,
    Response,
    ResponseException,
    enroute,
)

from ..aggregates import (
    Inventory,
    Product,
)


class ProductCommandService(CommandService):
    """Product Service class"""

    @staticmethod
    @enroute.broker.command("CreateProduct")
    @enroute.rest.command("/products", "POST")
    async def create_product(request: Request) -> Response:
        """Create a new product instance.

        :param request: The ``Request`` that contains the needed information to create the product.
        :return: A ``Response`` containing the already created product.
        """
        content = await request.content()
        title = content["title"]
        description = content["description"]
        price = content["price"]

        code = uuid4().hex.upper()[0:6]
        inventory = Inventory(amount=0)
        product = await Product.create(code, title, description, price, inventory)

        return Response(product)

    @staticmethod
    @enroute.rest.command("/products/{uuid}/inventory", "PUT")
    async def update_inventory(request: Request) -> Response:
        """Update inventory amount with a difference.

        :param request: ``Request`` that contains the needed information.
        :return: ``Response`` containing the updated product.
        """
        content = await request.content()
        uuid = content["uuid"]
        amount = content["amount"]

        product = await Product.get_one(uuid)
        product.inventory = Inventory(amount)
        await product.save()

        return Response(product)

    @staticmethod
    @enroute.rest.command("/products/{uuid}/inventory", "PATCH")
    async def update_inventory_diff(request: Request) -> Response:
        """Update inventory amount with a difference.

        :param request: ``Request`` that contains the needed information.
        :return: ``Response`` containing the updated product.
        """
        content = await request.content()
        uuid = content["uuid"]
        amount_diff = content["amount_diff"]

        product = await Product.get_one(uuid)
        product.inventory = Inventory(product.inventory.amount + amount_diff)
        await product.save()

        return Response(product)

    @staticmethod
    @enroute.broker.command("GetProducts")
    @enroute.rest.command("/products", "GET")
    async def get_products(request: Request) -> Response:
        """Get products.

        :param request: The ``Request`` instance that contains the product identifiers.
        :return: A ``Response`` instance containing the requested products.
        """
        _Query = ModelType.build("Query", {"uuids": list[UUID]})
        try:
            content = await request.content(model_type=_Query)
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        uuids = content["uuids"]

        try:
            values = {v.uuid: v async for v in Product.get(uuids=uuids)}
            products = [values[uuid] for uuid in uuids]
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting products: {exc!r}")

        return Response(products)

    @staticmethod
    @enroute.broker.command("GetProduct")
    @enroute.rest.command("/products/{uuid}", "GET")
    async def get_product(request: Request) -> Response:
        """Get product.

        :param request: The ``Request`` instance that contains the product identifier.
        :return: A ``Response`` instance containing the requested product.
        """
        _Query = ModelType.build("Query", {"uuid": UUID})
        try:
            content = await request.content(model_type=_Query)
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        uuid = content["uuid"]

        try:
            product = await Product.get_one(uuid)
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting the product: {exc!r}")

        return Response(product)

    @staticmethod
    @enroute.rest.command("/products/{uuid}", "DELETE")
    async def delete_product(request: Request) -> NoReturn:
        """Delete a product by identifier.

        :param request: A request containing the product identifier.
        :return: This method does not return anything.
        """
        content = await request.content()
        uuid = content["uuid"]

        try:
            product = await Product.get_one(uuid)
            await product.delete()
        except (MinosSnapshotDeletedAggregateException, MinosSnapshotAggregateNotFoundException):
            raise ResponseException(f"The product does not exist.")

    @enroute.broker.command("ReserveProducts")
    async def reserve_products(self, request: Request) -> NoReturn:
        """Reserve the requested quantities of products.

        :param: request: The ``Request`` instance that contains the quantities dictionary.
        :return: A ``Response containing a ``ValidProductInventoryList`` DTO.
        """
        content = await request.content()
        quantities = {UUID(k): v for k, v in content.quantities.items()}

        try:
            await self._reserve_products(quantities)
        except (MinosSnapshotAggregateNotFoundException, MinosSnapshotDeletedAggregateException) as exc:
            raise ResponseException(f"Some products do not exist: {exc!r}")
        except Exception as exc:
            raise ResponseException(f"There is not enough product amount: {exc!r}")

    async def _reserve_products(self, quantities: dict[UUID, int]):
        """Reserve product quantities.

        :param quantities: A dictionary in which the keys are the ``Product`` identifiers and the values are
        the number
            of units to be reserved.
        :return: ``True`` if all products can be satisfied or ``False`` otherwise.
        """
        feasible = True
        async for product in Product.get(uuids=set(quantities.keys())):
            inventory = product.inventory
            amount = inventory.amount
            if feasible and amount < quantities[product.uuid]:
                feasible = False
            amount -= quantities[product.uuid]
            product.inventory = Inventory(amount)
            await product.save()

        if not feasible:
            await self._reserve_products({k: -v for k, v in quantities.items()})
            raise ValueError("The reservation query could not be satisfied.")
