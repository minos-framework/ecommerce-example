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
    ResponseException,
    RestRequest,
    enroute,
)
from minos.saga import (
    SagaContext,
)

from .sagas import CREATE_CUSTOMER_SAGA
from ..jwt_env import (
    JWT_ALGORITHM,
    SECRET,
)
from .sagas import (
    CREATE_CUSTOMER_SAGA,
)


class CredentialsCommandService(CommandService):
    """Login Command Service class"""

    @enroute.rest.command("/login", "POST")
    async def create_credentials(self, request: Request) -> Response:
        content = await request.content()

        uuid = await self.saga_manager.run(
            definition=CREATE_CUSTOMER_SAGA,
            context=SagaContext(
                username=content["username"],
                password=content["password"],
                name=content["name"],
                surname=content["surname"],
                address=content["address"],
            ),
        )

        return Response(uuid)

    @enroute.rest.command("/token", "POST")
    async def validate_jwt(self, request: RestRequest) -> Response:
        auth_type, jwt_token = request.raw_request.headers["Authorization"].split()

        if auth_type == "Bearer":
            try:
                payload = jwt.decode(jwt_token, SECRET, algorithms=[JWT_ALGORITHM])
            except InvalidSignatureError as exc:
                raise ResponseException(exc.args[0])
            else:
                return Response(payload)
