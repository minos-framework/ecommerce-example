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

    TEST_USER = "test_user"
    TEST_PASSWORD = "test_password"

    repository: UserQueryRepository = Provide["user_repository"]

    @enroute.rest.query("/authentication/login", "GET")
    async def authenticate(self, request: RestRequest) -> Response:
        """Authenticate a User if valid user/password pair is given.

        :param request: The ``Request`` instance containing the User.
        :return: A ``Response`` containing the JWT.
        """
        auth_type, encoded_credentials = request.raw_request.headers["Authorization"].split()
        if auth_type == "Basic":
            user, password = base64.b64decode(encoded_credentials).decode().split(":")

            if self.valid_credentials(user, password):
                payload = {"sub": 1, "name": user, "iat": time.time()}
                jwt_token = jwt.encode(payload, self.SECRET, algorithm=self.JWT_ALGORITHM)

                return Response(jwt_token)
            else:
                # TODO: Where should I deal with this?
                error_msg = "Invalid username or password"
                return Response(error_msg)

    def valid_credentials(self, user: str, password: str):
        if user == self.TEST_USER and password == self.TEST_PASSWORD:
            return True
        else:
            return False

    @enroute.broker.event("UserCreated")
    async def user_created(self, request: Request) -> NoReturn:
        """Handle the product create and update events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        await self.repository.create(diff.username, diff.password, diff.active)
