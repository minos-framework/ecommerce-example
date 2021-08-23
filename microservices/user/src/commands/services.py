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
    User,
)


class UserCommandService(CommandService):
    """User Service class"""

    @staticmethod
    @enroute.rest.command("/users", "POST")
    @enroute.broker.command("CreateUser")
    async def create_user(request: Request) -> Response:
        """Create a new User instance.

        :param request: The ``Request`` that contains the needed information to create the User.
        :return: A ``Response`` containing the already created User.
        """
        content = await request.content()

        username = content["username"]
        password = content["password"]
        status = content["status"]
        address = Address(**content["address"])

        user = await User.create(username, password, status, address)

        return Response(user)
