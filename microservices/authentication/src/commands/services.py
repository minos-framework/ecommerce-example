import logging

from minos.aggregate import Condition
from minos.cqrs import CommandService
from minos.networks import (
    Request,
    Response,
    ResponseException,
    enroute,
)
from minos.saga import SagaContext

from ..aggregates import Credentials
from .sagas import CREATE_CREDENTIALS_SAGA

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
            execution = await self.saga_manager.run(
                definition=CREATE_CREDENTIALS_SAGA,
                context=SagaContext(username=username, password=password, metadata=metadata),
            )
        except Exception as exc:
            raise ResponseException(repr(exc))

        credentials = execution.context["credentials"]
        return Response({"user": credentials.user})

    @enroute.rest.command("/login", "DELETE")
    async def delete_credentials(self, request: Request) -> None:
        """Remove exising credentials based on a given identifier.

        :param request: A ``Request`` containing the username and password.

        :return:
        """
        content = await request.content()

        try:
            credentials = await Credentials.get(content["uuid"])
        except Exception as exc:
            raise ResponseException(f"The credentials could not be retrieved: {exc}")

        await credentials.delete()

    @enroute.broker.event("CustomerDeleted")
    async def user_deleted(self, request: Request) -> None:
        """Delete the associated credentials to the already deleted user.

        :param request: A ``Request`` containing a ``AggregateDiff`` instance.
        :return: This method does not return anything.
        """

        diff = await request.content()
        user = diff.uuid

        entries = {credentials async for credentials in Credentials.find(Condition.EQUAL("user", user))}

        if len(entries) == 0:
            return

        if len(entries) > 1:
            logger.warning(f"The user identified by {user!r} had multiple associated credentials")

        for credentials in entries:
            await credentials.delete()
