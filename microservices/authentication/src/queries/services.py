import base64
import time
from uuid import (
    UUID,
)

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
    Request,
    Response,
    RestRequest,
    enroute,
)

from ..jwt_env import (
    JWT_ALGORITHM,
    SECRET,
)
from .repositories import (
    UserQueryRepository,
)


class LoginQueryService(QueryService):
    repository: UserQueryRepository = Provide["user_repository"]

    @enroute.rest.query("/login", "GET")
    async def get_token(self, request: RestRequest) -> Response:
        auth_type, encoded_credentials = request.raw_request.headers["Authorization"].split()
        if auth_type == "Basic":
            username, password = base64.b64decode(encoded_credentials).decode().split(":")

            if await self.valid_credentials(username, password):
                jwt_token = await self.generate_token(username)
                return Response(jwt_token)
            else:
                return Response("Invalid username or password")

    async def generate_token(self, username):
        user = await self.repository.get_by_username(username)
        payload = {"sub": str(user["uuid"]), "name": user["username"], "iat": time.time()}
        jwt_token = jwt.encode(payload, SECRET, algorithm=JWT_ALGORITHM)
        return jwt_token

    async def valid_credentials(self, user: str, password: str) -> bool:
        return await self.repository.exist_credentials(user, password)

    @enroute.broker.event("UserCreated")
    async def user_created(self, request: Request) -> None:
        diff: AggregateDiff = await request.content()
        await self.repository.create_user(diff.uuid, diff.username, diff.password, diff.active)
