from minos.cqrs import (
    CommandService,
)
from minos.networks import (
    Request,
    Response,
    ResponseException,
    enroute,
)


class TicketCommandService(CommandService):
    """Ticket Service class"""

    @enroute.rest.command("/tickets", "POST")
    @enroute.broker.command("CreateTicket")
    async def create_ticket(self, request: Request) -> Response:
        """Create a new ticket.

        :param request: The ``Request`` instance to be use to compute the price.
        :return: A ``Response`` containing the created ticket.
        """
        content = await request.content()
        cart_uuid = content["cart_uuid"]

        try:
            ticket = await self.aggregate.create_ticket(cart_uuid)
        except ValueError:
            raise ResponseException("An error occurred during order creation.")

        return Response(ticket)
