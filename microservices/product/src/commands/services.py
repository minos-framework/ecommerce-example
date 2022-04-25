import logging
from uuid import (
    UUID,
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

logger = logging.getLogger(__name__)


class ProductCommandService(CommandService):
    """Product Service class"""

    @enroute.broker.command("CreateProduct")
    @enroute.rest.command("/products", "POST")
    async def create_product(self, request: Request) -> Response:
        """Create a new product instance.

        :param request: The ``Request`` that contains the needed information to create the product.
        :return: A ``Response`` containing the already created product.
        """
        content = await request.content()

        title = content["title"]
        description = content["description"]
        price = content["price"]

        product = await self.aggregate.create_product(title, description, price)

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

        product = self.aggregate.update_inventory(uuid, amount)

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

        product = self.aggregate.update_inventory_diff(uuid, amount_diff)

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

        uuid, amount, amount_diff = None, None, None
        if "amount_diff" in content:
            params = await request.params()
            uuid = params["uuid"]
            amount_diff = content["amount_diff"]
        else:
            amount = content["amount"]

        return await self.aggregate.check_positive_inventory(uuid, amount, amount_diff)

    @enroute.rest.command(f"/products/{{uuid:{UUID_REGEX.pattern}}}", "PUT")
    async def update_product(self, request: HttpRequest) -> Response:
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

        product = self.aggregate.update_product(uuid, title, description, price)
        return Response(product)

    @enroute.rest.command(f"/products/{{uuid:{UUID_REGEX.pattern}}}", "PATCH")
    async def update_product_diff(self, request: HttpRequest) -> Response:
        """Update product information with a difference.

        :param request: ``Request`` that contains the needed information.
        :return: ``Response`` containing the updated product.
        """
        content = await request.content()
        params = await request.params()
        uuid = params["uuid"]
        product = await self.aggregate.update_product_diff(uuid, content)

        await product.save()

        return Response(product)

    @enroute.rest.command(f"/products/{{uuid:{UUID_REGEX.pattern}}}", "DELETE")
    async def delete_product(self, request: HttpRequest) -> None:
        """Delete a product by identifier.

        :param request: A request containing the product identifier.
        :return: This method does not return anything.
        """
        params = await request.params()
        uuid = params["uuid"]

        try:
            self.aggregate.delete_product(uuid)
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
            await self.aggregate.reserve(quantities)
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
            await self.aggregate.purchase(quantities)
        except (NotFoundException, AlreadyDeletedException) as exc:
            raise ResponseException(f"Some products do not exist: {exc!r}")
        except Exception as exc:
            raise ResponseException(f"There is not enough product amount: {exc!r}")
