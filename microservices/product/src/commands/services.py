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
    UUID_REGEX,
    EntitySet,
    MinosSnapshotAggregateNotFoundException,
    MinosSnapshotDeletedAggregateException,
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
    Review,
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
        reviews = EntitySet()
        product = await Product.create(code, title, description, price, inventory, reviews)

        return Response(product)

    @staticmethod
    @enroute.rest.command(f"/products/{{uuid:{UUID_REGEX.pattern}}}/reviews", "POST")
    async def add_review(request: Request) -> Response:
        content = await request.content()
        uuid = content["uuid"]
        stars = content["stars"]
        message = content["message"]

        product = await Product.get_one(uuid)

        review = Review(stars=stars, message=message)
        product.reviews.add(review)
        await product.save()

        return Response(product)

    @staticmethod
    @enroute.rest.command(f"/products/{{uuid:{UUID_REGEX.pattern}}}/inventory", "PUT")
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
    @enroute.rest.command(f"/products/{{uuid:{UUID_REGEX.pattern}}}/inventory", "PATCH")
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
    @enroute.rest.command(f"/products/{{uuid:{UUID_REGEX.pattern}}}", "PUT")
    async def update_product(request: Request) -> Response:
        """Update product information.

        :param request: ``Request`` that contains the needed information.
        :return: ``Response`` containing the updated product.
        """
        content = await request.content()
        uuid = content["uuid"]
        title = content["title"]
        description = content["description"]
        price = content["price"]

        product = await Product.get_one(uuid)
        product.title = title
        product.description = description
        product.price = price

        await product.save()

        return Response(product)

    @staticmethod
    @enroute.rest.command(f"/products/{{uuid:{UUID_REGEX.pattern}}}", "PATCH")
    async def update_product_diff(request: Request) -> Response:
        """Update product information with a difference.

        :param request: ``Request`` that contains the needed information.
        :return: ``Response`` containing the updated product.
        """
        content = await request.content()
        uuid = content["uuid"]
        product = await Product.get_one(uuid)

        if "title" in content or hasattr(content, "title"):
            title = content["title"]
            product.title = title
        if "description" in content or hasattr(content, "description"):
            description = content["description"]
            product.description = description
        if "price" in content or hasattr(content, "price"):
            price = content["price"]
            product.price = price

        await product.save()

        return Response(product)

    @staticmethod
    @enroute.rest.command(f"/products/{{uuid:{UUID_REGEX.pattern}}}", "DELETE")
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
