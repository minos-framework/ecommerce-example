from aiohttp import web
from minos.api_gateway.common import (
    MinosConfig,
)
import jwt
from jwt.exceptions import InvalidSignatureError

SECRET = "secret"


class LoginController:
    async def login(self, request: web.Request, config: MinosConfig) -> web.Response:
        token = jwt.encode({"some": "payload"}, SECRET, algorithm="HS256")
        return web.Response(text=encoded_jwt)

    async def test_endpoint(self, request: web.Request, config: MinosConfig) -> web.Response:
        token = request.headers['Authorization'].split()[-1]
        try:
            msg = jwt.decode(token, SECRET, algorithms=["HS256"])
        except InvalidSignatureError as e:
            msg = e
        return web.Response(text=str(msg))
