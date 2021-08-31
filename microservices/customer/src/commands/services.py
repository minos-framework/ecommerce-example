"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""

from minos.cqrs import CommandService
from minos.networks import (
    Request,
    Response,
    enroute,
)

from ..aggregates import (
    Address,
    Customer,
)


class CustomerCommandService(CommandService):
    """Customer Service class"""

    @staticmethod
    @enroute.rest.command("/customer", "POST")
    @enroute.broker.command("CreateCustomer")
    async def create_customer(request: Request) -> Response:
        """Create a new Customer instance.

        :param request: The ``Request`` that contains the needed information to create the Customer.
        :return: A ``Response`` containing the already created Customer.
        """
        content = await request.content()

        name = content["name"]
        surname = content["surname"]
        address = Address(**content["address"])

        customer = await Customer.create(name, surname, address)

        return Response(customer)
