"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import (
    UUID,
)

from minos.common import (
    ModelType,
)
from minos.cqrs import (
    QueryService,
)
from minos.networks import (
    Request,
    Response,
    ResponseException,
    enroute,
)


class UserQueryService(QueryService):
    """User Query Service class"""

    @staticmethod
    @enroute.broker.query("GetUsers")
    async def get_users(request: Request) -> Response:
        """Get users.

        :param request: The ``Request`` instance that contains the user identifiers.
        :return: A ``Response`` instance containing the requested users.
        """
        try:
            content = await request.content(model_type=ModelType.build("Query", {"uuids": list[UUID]}))
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        try:
            from ..aggregates import (
                User,
            )

            iterable = User.get(uuids=content["uuids"])
            values = {v.uuid: v async for v in iterable}
            users = [values[uuid] for uuid in content["uuids"]]
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting users: {exc!r}")

        return Response(users)

    @staticmethod
    @enroute.broker.query("GetUser")
    async def get_user(request: Request) -> Response:
        """Get user.

        :param request: The ``Request`` instance that contains the user identifier.
        :return: A ``Response`` instance containing the requested user.
        """
        try:
            content = await request.content(model_type=ModelType.build("Query", {"uuid": UUID}))
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        try:
            from ..aggregates import (
                User,
            )

            user = await User.get_one(content["uuid"])
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting the user: {exc!r}")

        return Response(user)
