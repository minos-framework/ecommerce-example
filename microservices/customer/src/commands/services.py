from minos.common import UUID_REGEX
from minos.cqrs import CommandService
from minos.networks import (
    HttpRequest,
    Request,
    Response,
    ResponseException,
    enroute,
)


class CustomerCommandService(CommandService):
    """Customer Service class"""

    @enroute.rest.command("/customers", "POST")
    @enroute.broker.command("CreateCustomer")
    async def create_customer(self, request: Request) -> Response:
        """Create a new Customer instance.

        :param request: The ``Request`` that contains the needed information to create the Customer.
        :return: A ``Response`` containing the already created Customer.
        """
        content = await request.content()

        name = content["name"]
        surname = content["surname"]
        address = content["address"]

        customer = await self.aggregate.create_customer(name, surname, address)

        return Response(customer)

    @enroute.rest.command(f"/customers/{{uuid:{UUID_REGEX.pattern}}}", "DELETE")
    @enroute.broker.command("DeleteCustomer")
    async def delete_customer(self, request: Request) -> None:
        """Remove a Customer instance.

        :param request: The ``Request`` that contains the needed customer identifier.
        :return: This method does not return anything.
        """

        try:
            if isinstance(request, HttpRequest):
                params = await request.params()
                uuid = params["uuid"]
            else:
                content = await request.content()
                uuid = content["uuid"]
        except Exception:
            raise ResponseException("The given request could not be parsed.")

        try:
            await self.aggregate.delete_customer(uuid)
        except Exception:
            raise ResponseException("The requested user could not be retrieved from the database.")
