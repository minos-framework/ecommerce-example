import logging
from uuid import (
    UUID,
    uuid4,
)

from minos.aggregate import (
    AlreadyDeletedException,
    NotFoundException,
)
from minos.common import (
    UUID_REGEX,
)
from minos.cqrs import (
    CommandService,
)
from minos.networks import (
    HttpRequest,
    Request,
    Response,
    ResponseException,
    enroute,
)

from ..aggregates import (
    Inventory,
    Product,
)

logger = logging.getLogger(__name__)


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

        code = uuid4().hex.upper()[0:6]
        title = content["title"]
        description = content["description"]
        price = content["price"]
        inventory = Inventory.empty()

        product = await Product.create(code, title, description, price, inventory)

        return Response(product)

    @enroute.rest.command(f"/products/{{uuid:{UUID_REGEX.pattern}}}/inventory", "PUT")
    async def update_inventory(self, request: HttpRequest) -> Response:
        """Update inventory amount with a difference.

        :param request: ``Request`` that contains the needed information.
        :return: ``Response`` containing the updated product.
        """
        content = await request.content()
        params = await request.params()
        uuid = params["uuid"]
        amount = content["amount"]

        product = await Product.get(uuid)
        product.set_inventory_amount(amount)
        await product.save()

        return Response(product)

    @enroute.rest.command(f"/products/{{uuid:{UUID_REGEX.pattern}}}/inventory", "PATCH")
    async def update_inventory_diff(self, request: HttpRequest) -> Response:
        """Update inventory amount with a difference.

        :param request: ``Request`` that contains the needed information.
        :return: ``Response`` containing the updated product.
        """
        content = await request.content()
        params = await request.params()
        uuid = params["uuid"]
        amount_diff = content["amount_diff"]

        product = await Product.get(uuid)
        product.update_inventory_amount(amount_diff)
        await product.save()

        return Response(product)

    @update_inventory.check(max_attempts=1)
    @update_inventory_diff.check()
    async def check_positive_inventory(self, request: HttpRequest) -> bool:
        """Check if the inventory is positive.

        :param request: The ``Request`` that contains the needed information.
        :return:  ``True`` if is positive or ``False`` otherwise.
        """
        logger.info("Checking positive inventory...")
        content = await request.content()

        if "amount_diff" in content:
            params = await request.params()
            uuid = params["uuid"]
            product = await Product.get(uuid)
            amount_diff = content["amount_diff"]
            amount = product.inventory.amount + amount_diff
        else:
            amount = content["amount"]

        return amount >= 0

    @staticmethod
    @enroute.rest.command(f"/products/{{uuid:{UUID_REGEX.pattern}}}", "PUT")
    async def update_product(request: HttpRequest) -> Response:
        """Update product information.

        :param request: ``Request`` that contains the needed information.
        :return: ``Response`` containing the updated product.
        """
        content = await request.content()
        params = await request.params()
        uuid = params["uuid"]
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
    async def update_product_diff(request: HttpRequest) -> Response:
        """Update product information with a difference.

        :param request: ``Request`` that contains the needed information.
        :return: ``Response`` containing the updated product.
        """
        content = await request.content()
        params = await request.params()
        uuid = params["uuid"]
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
    async def delete_product(request: HttpRequest) -> None:
        """Delete a product by identifier.

        :param request: A request containing the product identifier.
        :return: This method does not return anything.
        """
        params = await request.params()
        uuid = params["uuid"]

        try:
            product = await Product.get(uuid)
            await product.delete()
        except (AlreadyDeletedException, NotFoundException):
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
        except (NotFoundException, AlreadyDeletedException) as exc:
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
        except (NotFoundException, AlreadyDeletedException) as exc:
            raise ResponseException(f"Some products do not exist: {exc!r}")
        except Exception as exc:
            raise ResponseException(f"There is not enough product amount: {exc!r}")
