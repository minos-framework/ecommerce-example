"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from datetime import (
    datetime,
)

from minos.cqrs import (
    CommandService,
)
from minos.networks import (
    Request,
    Response,
    enroute,
)
from minos.common import (
    UUID_REGEX, ValueObjectSet,
)
from ..aggregates import (
    Address,
    User,
    CreditCard,
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
        created_at = datetime.now()
        credit_cards = ValueObjectSet()

        user = await User.create(username, password, status, address, created_at, credit_cards)

        return Response(user)

    @staticmethod
    @enroute.rest.command(f"/users/{{uuid:{UUID_REGEX.pattern}}}/credit_card", "POST")
    async def add_credit_card(request: Request) -> Response:
        """Create a new User instance.

        :param request: The ``Request`` that contains the needed information to create the User.
        :return: A ``Response`` containing the already created User.
        """
        content = await request.content()
        uuid = content["uuid"]
        name = content["name"]

        user = await User.get_one(uuid)

        credit_card = CreditCard(name=name)
        user.credit_cards.add(credit_card)
        await user.save()

        return Response(user)
