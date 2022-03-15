import base64
import time

import jwt
from dependency_injector.wiring import (
    Provide,
    inject,
)
from jwt.exceptions import (
    InvalidTokenError,
)
from minos.aggregate import (
    Event,
)
from minos.cqrs import (
    QueryService,
)
from minos.networks import (
    Request,
    Response,
    ResponseException,
    HttpRequest,
    enroute,
)

from ..jwt_env import (
    JWT_ALGORITHM,
    SECRET,
)
from .repositories import (
    CredentialsQueryRepository,
)


class CredentialsQueryService(QueryService):
    """Credentials Query Service class."""

    @inject
    def __init__(self, *args, repository: CredentialsQueryRepository = Provide["credentials_repository"], **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = repository

    @enroute.rest.query("/login", "GET")
    async def generate_token(self, request: HttpRequest) -> Response:
        """Get token from the given request.

        :param request: A ``HttpRequest`` containing the credentials on its headers.
        :return: A ``Response`` containing the token.
        """
        auth_type, encoded_credentials = request.headers["Authorization"].split()
        if auth_type != "Basic":
            raise ResponseException("Only 'Basic Authentication' is supported")

        username, password = base64.b64decode(encoded_credentials).decode().split(":")

        if not await self._validate_credentials(username, password):
            raise ResponseException("Invalid username or password")

        token = await self._generate_token(username)

        return Response({"token": token})

    async def _validate_credentials(self, username: str, password: str) -> bool:
        """Check if the given credentials are valid.

        :param username: The username.
        :param password: The password.
        :return: ``True`` if are valid or ``False`` otherwise.
        """
        return await self.repository.exist_credentials(username, password)

    async def _generate_token(self, username: str) -> str:
        """Generate a token for credentials identified by the given username.

        :param username: The username that identifies the credentials.
        :return: A token encoded as an string value.
        """
        credentials = await self.repository.get_by_username(username)

        payload = {"sub": str(credentials["user"]), "name": credentials["username"], "iat": time.time()}

        return jwt.encode(payload, SECRET, algorithm=JWT_ALGORITHM)

    @enroute.rest.query("/token", "POST")
    async def validate_token(self, request: HttpRequest) -> Response:
        """Validate if the given ``jwt`` token is valid.

        :param request: A ``HttpRequest`` containing the token in headers.
        :return: The response containing the payload if everything is fine or an exception otherwise.
        """
        auth_type, token = request.headers["Authorization"].split()

        if auth_type != "Bearer":
            raise ResponseException("Only 'Bearer Authentication' is supported")

        try:
            payload = jwt.decode(token, SECRET, algorithms=[JWT_ALGORITHM])
        except InvalidTokenError as exc:
            raise ResponseException(exc.args[0])

        return Response(payload)

    @enroute.broker.query("GetByUsername")
    async def get_by_username(self, request: Request) -> Response:
        content = await request.content()
        username = content["username"]
        credentials = await self.repository.get_by_username(username)
        if credentials:
            return Response(credentials["username"])
        else:
            raise ResponseException("Username does not exist")

    @enroute.broker.query("UniqueUsername")
    async def unique_username(self, request: Request) -> Response:
        content = await request.content()
        username = content["username"]
        credentials = await self.repository.get_by_username(username)
        if credentials:
            raise ResponseException("'username' already exists")
        else:
            return Response(True)

    @enroute.broker.event("CredentialsCreated")
    async def credentials_created(self, request: Request) -> None:
        """Handle the ``CredentialsCreated`` domain event.

        :param request: A ``Request`` instance containing the ``Event``.
        :return: This method does not return anything.
        """
        diff: Event = await request.content()
        await self.repository.create_credentials(diff.uuid, diff.username, diff.password, diff.active, diff.user)
