from minos.cqrs import (
    CommandService,
)
from minos.networks import (
    Request,
    Response,
    ResponseException,
    enroute,
)
from minos.saga import (
    SagaContext,
    SagaStatus,
)

from .sagas import (
    _CREATE_TICKET,
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

        execution = await self.saga_manager.run(
            _CREATE_TICKET, context=SagaContext(cart_uuid=cart_uuid), raise_on_error=False
        )

        if execution.status == SagaStatus.Finished:
            return Response(execution.context["ticket"])
        else:
            raise ResponseException("An error occurred during order creation.")
