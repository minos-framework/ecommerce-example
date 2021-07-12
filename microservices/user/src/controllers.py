"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import (
    ModelType,
    Request,
    Response,
    ResponseException,
)

from .services import (
    UserService,
)

_Query = ModelType.build("Query", {"ids": list[int]})


class UserController:
    """Ticket Controller class"""

    @staticmethod
    async def create_user(request: Request) -> Response:
        """Create a new ``User`` instance.

        :param request: The ``Request`` containing the list of product identifiers to be included in the ``User``.
        :return: A ``Response`` containing the ``UUID`` that identifies the ``SagaExecution``.
        """
        content = await request.content()
        uuid = await UserService().create_user(**content)
        return Response(str(uuid))

    @staticmethod
    async def get_users(request: Request) -> Response:
        """Get a list of users by id.

        :param request: The ``Request`` instance containing the list of ``User`` identifiers.
        :return: A ``Response`` containing the list of ``User`` instances.
        """
        try:
            content = await request.content(model_type=_Query)
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        try:
            users = await UserService().get_users(**content)
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting users: {exc!r}")

        return Response(users)
