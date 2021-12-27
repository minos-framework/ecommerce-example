from dependency_injector.wiring import (
    Provide,
)
from minos.aggregate import (
    AggregateDiff,
)
from minos.common import (
    UUID_REGEX,
)
from minos.cqrs import (
    QueryService,
)
from minos.networks import (
    Request,
    Response,
    RestRequest,
    enroute,
)

from .repositories import (
    TicketQueryRepository,
)


class TicketQueryService(QueryService):
    """Ticket Query Service class."""

    repository: TicketQueryRepository = Provide["ticket_repository"]

    @enroute.broker.query("GetTicketQRS")
    @enroute.rest.query(f"/tickets/{{uuid:{UUID_REGEX.pattern}}}", "GET")
    async def get_ticket(self, request: Request) -> Response:
        """Get ticket.

        :param request: The ``Request`` instance that contains the ticket identifier.
        :return: A ``Response`` instance containing the requested ticket.
        """
        if isinstance(request, RestRequest):
            params = await request.params()
            uuid = params["uuid"]
        else:
            content = await request.content()
            uuid = content["uuid"]

        res = await self.repository.get_ticket(uuid)

        return Response(res)

    @enroute.broker.event("TicketCreated")
    async def ticket_created_or_updated(self, request: Request) -> None:
        """Handle the ticket creation events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        uuid = diff.uuid
        version = diff["version"]
        code = diff["code"]
        total_price = diff["total_price"]
        entries = diff["entries"]

        await self.repository.insert(uuid, version, code, total_price, entries)

    @enroute.broker.event("TicketDeleted")
    async def ticket_deleted(self, request: Request) -> None:
        """Handle the ticket delete events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

        print(diff)
