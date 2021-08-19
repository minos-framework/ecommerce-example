import base64
import time
from typing import NoReturn

import jwt
from dependency_injector.wiring import (
    Provide,
)
from minos.common import (
    AggregateDiff,
)
from minos.cqrs import (
    QueryService,
)
from minos.networks import (
    RestRequest,
    Request,
    Response,
    enroute,
)

from .repositories import UserQueryRepository


class LoginQueryService(QueryService):
    """Login Query Service class."""

    JWT_ALGORITHM = "HS256"
    SECRET = "secret"

    repository: UserQueryRepository = Provide["user_repository"]

    @enroute.rest.query("/authentication/login", "GET")
    async def authenticate(self, request: RestRequest) -> Response:
        auth_type, encoded_credentials = request.raw_request.headers["Authorization"].split()
        if auth_type == "Basic":
            user, password = base64.b64decode(encoded_credentials).decode().split(":")

            if await self.valid_credentials(user, password):
                payload = {"sub": 1, "name": user, "iat": time.time()}
                jwt_token = jwt.encode(payload, self.SECRET, algorithm=self.JWT_ALGORITHM)

                return Response(jwt_token)
            else:
                # TODO: Where should I deal with this?
                error_msg = "Invalid username or password"
                return Response(error_msg)

    async def valid_credentials(self, user: str, password: str):
        return await self.repository.exist_credentials(user, password)

    @enroute.broker.event("UserCreated")
    async def user_created(self, request: Request) -> None:
        diff: AggregateDiff = await request.content()
        await self.repository.create(diff.username, diff.password, diff.active)
