import logging

from minos.aggregate import (
    Condition,
)
from minos.cqrs import (
    CommandService,
)
from minos.networks import (
    Request,
    Response,
    ResponseException,
    enroute,
)

from ..aggregates import (
    Credentials,
)

logger = logging.getLogger(__name__)


class CredentialsCommandService(CommandService):
    """Credentials Command Service class"""

    @enroute.rest.command("/login", "POST")
    async def create_credentials(self, request: Request) -> Response:
        """Create new credentials based on a given username and password.

        :param request: A ``Request`` containing the username and password.

        :return:
        """
        content = await request.content()

        username = content["username"]
        password = content["password"]
        metadata = {k: v for k, v in content.items() if k not in {"username", "password"}}

        try:
            credentials = await self.aggregate.create_credentials(username, password, metadata)
        except Exception as exc:
            raise ResponseException(repr(exc))

        return Response({"user": credentials.user})

    @enroute.rest.command("/login", "DELETE")
    async def delete_credentials(self, request: Request) -> None:
        """Remove exising credentials based on a given identifier.

        :param request: A ``Request`` containing the username and password.

        :return:
        """
        content = await request.content()

        try:
            await self.aggregate.delete_credentials(content["uuid"])
        except Exception as exc:
            raise ResponseException(f"The credentials could not be retrieved: {exc}")

    @enroute.broker.event("CustomerDeleted")
    async def user_deleted(self, request: Request) -> None:
        """Delete the associated credentials to the already deleted user.

        :param request: A ``Request`` containing a ``Delta`` instance.
        :return: This method does not return anything.
        """

        diff = await request.content()
        user = diff.uuid

        await self.aggregate.delete_credentials_by_user(user)
