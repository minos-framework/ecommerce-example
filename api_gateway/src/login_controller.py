import base64
import time

import jwt
from aiohttp import (
    web,
)
from jwt.exceptions import (
    InvalidSignatureError,
)
from minos.api_gateway.common import (
    MinosConfig,
)

JWT_ALGORITHM = "HS256"
SECRET = "secret"

TEST_USER = "test_user"
TEST_PASSWORD = "test_password"


def valid_credentials(user: str, password: str):
    if user == TEST_USER and password == TEST_PASSWORD:
        return True
    else:
        return False


class AuthController:
    async def login(self, request: web.Request, config: MinosConfig) -> web.Response:
        auth_type, encoded_credentials = request.headers["Authorization"].split()
        if auth_type == "Basic":
            user, password = base64.b64decode(encoded_credentials).decode().split(":")

        if valid_credentials(user, password):
            payload = {"sub": 1, "name": user, "iat": time.time()}  # TODO: Add actual User uuid
            jwt_token = jwt.encode(payload, SECRET, algorithm=JWT_ALGORITHM)

            return web.Response(text=jwt_token)
        else:
            # TODO: Where should I deal with this?
            error_msg = "Invalid username or password"
            return web.Response(text=error_msg)

    async def test_endpoint(self, request: web.Request, config: MinosConfig) -> web.Response:
        auth_type, jwt_token = request.headers["Authorization"].split()

        if auth_type == "Bearer":
            try:
                payload = jwt.decode(jwt_token, SECRET, algorithms=[JWT_ALGORITHM])
                # TODO: Redirect
                return web.Response(text=str(payload))
            except InvalidSignatureError as e:
                error_msg = str(e)
                return web.Response(text=error_msg)
