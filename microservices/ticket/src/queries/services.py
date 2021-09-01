"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import (
    NoReturn,
)
from uuid import (
    UUID,
)

from dependency_injector.wiring import (
    Provide,
)
from minos.common import (
    UUID_REGEX,
    AggregateDiff,
    ModelType,
)
from minos.cqrs import (
    QueryService,
)
from minos.networks import (
    Request,
    Response,
    ResponseException,
    enroute,
)

from .repositories import (
    TicketQueryRepository,
)


class TicketQueryService(QueryService):
    """Ticket Query Service class."""

    repository: TicketQueryRepository = Provide["ticket_repository"]

    @staticmethod
    @enroute.broker.query("GetTickets")
    @enroute.rest.query("/tickets", "GET")
    async def get_tickets(request: Request) -> Response:
        """Get tickets.

        :param request: The ``Request`` instance that contains the ticket identifiers.
        :return: A ``Response`` instance containing the requested tickets.
        """
        try:
            content = await request.content(model_type=ModelType.build("Query", {"uuids": list[UUID]}))
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        try:
            from ..aggregates import (
                Ticket,
            )

            iterable = Ticket.get(uuids=content["uuids"])
            values = {v.uuid: v async for v in iterable}
            tickets = [values[uuid] for uuid in content["uuids"]]
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting tickets: {exc!r}")

        return Response(tickets)

    @staticmethod
    @enroute.broker.query("GetTicket")
    @enroute.rest.query(f"/tickets/{{uuid:{UUID_REGEX.pattern}}}", "GET")
    async def get_ticket(request: Request) -> Response:
        """Get ticket.

        :param request: The ``Request`` instance that contains the ticket identifier.
        :return: A ``Response`` instance containing the requested ticket.
        """
        try:
            content = await request.content(model_type=ModelType.build("Query", {"uuid": UUID}))
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        try:
            from ..aggregates import (
                Ticket,
            )

            ticket = await Ticket.get_one(content["uuid"])
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting the ticket: {exc!r}")

        return Response(ticket)

    @enroute.broker.event("TicketCreated")
    @enroute.broker.event("TicketUpdated")
    async def ticket_created_or_updated(self, request: Request) -> NoReturn:
        """Handle the ticket creation events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        uuid = diff.uuid
        total_price = diff["total_price"]

        await self.repository.insert_ticket_amount(uuid, total_price)

    @enroute.broker.event("TicketDeleted")
    async def ticket_deleted(self, request: Request) -> NoReturn:
        """Handle the ticket delete events.
        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

        await self.repository.delete(diff.uuid)
