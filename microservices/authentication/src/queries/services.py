import base64
import time

import jwt
from dependency_injector.wiring import (
    Provide,
    inject,
)
from minos.common import AggregateDiff
from minos.cqrs import QueryService
from minos.networks import (
    Request,
    Response,
    ResponseException,
    RestRequest,
    enroute,
)

from ..jwt_env import (
    JWT_ALGORITHM,
    SECRET,
)
from .repositories import CredentialsQueryRepository


class CredentialsQueryService(QueryService):
    @inject
    def __init__(self, *args, repository: CredentialsQueryRepository = Provide["credentials_repository"], **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = repository

    @enroute.rest.query("/login", "GET")
    async def get_token(self, request: RestRequest) -> Response:
        auth_type, encoded_credentials = request.raw_request.headers["Authorization"].split()
        if auth_type == "Basic":
            username, password = base64.b64decode(encoded_credentials).decode().split(":")

            if await self.valid_credentials(username, password):
                jwt_token = await self.generate_token(username)
                return Response(jwt_token)
            else:
                raise ResponseException("Invalid username or password")

    async def generate_token(self, username) -> str:
        credentials = await self.repository.get_by_username(username)
        payload = {"sub": str(credentials["uuid"]), "name": credentials["username"], "iat": time.time()}
        jwt_token = jwt.encode(payload, SECRET, algorithm=JWT_ALGORITHM)
        return jwt_token

    async def valid_credentials(self, username: str, password: str) -> bool:
        return await self.repository.exist_credentials(username, password)

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
        diff: AggregateDiff = await request.content()
        await self.repository.create_credentials(diff.uuid, diff.username, diff.password, diff.active)
