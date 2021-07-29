"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""

from minos.common import (
    Request,
    Response,
    Service, ResponseException, ModelType,
)
from ..aggregates import (
    User,
)


class UserQueryService(Service):
    def get_user(self, request: Request) -> Response:
        _Query = ModelType.build("Query", {"username": str})

        try:
            content = await request.content(model_type=_Query)
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        username = content["username"]

        try:
            values = User.get(username=username)
            products = [values[uuid] for uuid in uuids]
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting products: {exc!r}")
