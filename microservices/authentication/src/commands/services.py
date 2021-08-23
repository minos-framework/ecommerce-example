import jwt
from jwt.exceptions import (
    InvalidSignatureError,
)
from minos.cqrs import (
    CommandService,
)
from minos.networks import (
    Request,
    Response,
    RestRequest,
    enroute,
)
from src import (
    User,
)

from ..jwt_env import (
    JWT_ALGORITHM,
    SECRET,
)


class LoginCommandService(CommandService):
    """Login Command Service class"""

    @enroute.rest.command("/login", "POST")
    async def create_user(self, request: Request) -> Response:
        content = await request.content()
        username = content["username"]
        password = content["password"]

        user = await User.create(username, password, active=True)

        return Response(user)

    @enroute.rest.command("/token", "POST")
    async def validate_jwt(self, request: RestRequest) -> Response:
        auth_type, jwt_token = request.raw_request.headers["Authorization"].split()

        if auth_type == "Bearer":
            try:
                payload = jwt.decode(jwt_token, SECRET, algorithms=[JWT_ALGORITHM])
                return Response(str(payload))
            except InvalidSignatureError as exc:
                return Response(exc)
