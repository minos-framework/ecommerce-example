from aiohttp import web
from minos.api_gateway.common import (
    MinosConfig,
)
import jwt


class LoginController:
    async def login(self, request: web.Request, config: MinosConfig):
        encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
        print(encoded_jwt)
        print(jwt.decode(encoded_jwt, "secret", algorithms=["HS256"]))
