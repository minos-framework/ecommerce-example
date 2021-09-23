from uuid import (
    UUID,
)

from minos.common import (
    UUID_REGEX,
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

        product = await Product.create(title, description, price)

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

        product = await Product.get(uuid)
        product.set_inventory_amount(amount)
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

        product = await Product.get(uuid)
        product.update_inventory_amount(amount_diff)
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

        product = await Product.get(uuid)
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
        product = await Product.get(uuid)

        if "title" in content:
            product.title = content["title"]

        if "description" in content:
            product.description = content["description"]

        if "price" in content:
            product.price = content["price"]

        await product.save()

        return Response(product)

    @staticmethod
    @enroute.rest.command(f"/products/{{uuid:{UUID_REGEX.pattern}}}", "DELETE")
    async def delete_product(request: Request) -> None:
        """Delete a product by identifier.

        :param request: A request containing the product identifier.
        :return: This method does not return anything.
        """
        content = await request.content()
        uuid = content["uuid"]

        try:
            product = await Product.get(uuid)
            await product.delete()
        except (MinosSnapshotDeletedAggregateException, MinosSnapshotAggregateNotFoundException):
            raise ResponseException("The product does not exist.")

    @enroute.broker.command("ReserveProducts")
    async def reserve_products(self, request: Request) -> None:
        """Reserve the requested quantities of products.

        :param: request: The ``Request`` instance that contains the quantities dictionary.
        :return: A ``Response containing a ``ValidProductInventoryList`` DTO.
        """
        content = await request.content()

        quantities = {UUID(k): v for k, v in content["quantities"].items()}

        try:
            await Product.reserve(quantities)
        except (MinosSnapshotAggregateNotFoundException, MinosSnapshotDeletedAggregateException) as exc:
            raise ResponseException(f"Some products do not exist: {exc!r}")
        except Exception as exc:
            raise ResponseException(f"There is not enough product amount: {exc!r}")

    @enroute.broker.command("PurchaseProducts")
    async def purchase_products(self, request: Request) -> None:
        """Purchase the requested quantities of products.

        :param: request: The ``Request`` instance that contains the quantities dictionary.
        :return: A ``Response containing a ``ValidProductInventoryList`` DTO.
        """
        content = await request.content()

        quantities = {UUID(k): v for k, v in content["quantities"].items()}

        try:
            await Product.purchase(quantities)
        except (MinosSnapshotAggregateNotFoundException, MinosSnapshotDeletedAggregateException) as exc:
            raise ResponseException(f"Some products do not exist: {exc!r}")
        except Exception as exc:
            raise ResponseException(f"There is not enough product amount: {exc!r}")
