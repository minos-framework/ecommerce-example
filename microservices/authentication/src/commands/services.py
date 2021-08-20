from minos.cqrs import CommandService
from minos.networks import Request, Response, enroute
from src import User


class LoginCommandService(CommandService):
    """Login Command Service class"""

    @enroute.rest.command("/login", "POST")
    async def create_user(self, request: Request) -> Response:
        """Create a new ``Order`` instance.

        :param request: The ``Request`` containing the list of product identifiers to be included in the ``Order``.
        :return: A ``Response`` containing the ``UUID`` that identifies the ``SagaExecution``.
        """
        content = await request.content()
        username = content["username"]
        password = content["password"]

        user = await User.create(username, password, active=True)

        return Response(user)
