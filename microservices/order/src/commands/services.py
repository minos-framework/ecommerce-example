from minos.cqrs import (
    CommandService,
)
from minos.networks import (
    Request,
    Response,
    ResponseException,
    enroute,
)


class OrderCommandService(CommandService):
    """Ticket Service class"""

    @enroute.rest.command("/orders", "POST")
    @enroute.broker.command("CreateOrder")
    async def create_order(self, request: Request) -> Response:
        """Create a new ``Order`` instance.
        :param request: The ``Request`` containing the list of product identifiers to be included in the ``Order``.
        :return: A ``Response`` containing the ``UUID`` that identifies the ``SagaExecution``.
        """
        content = await request.content()
        cart_uuid = content["cart"]
        customer_uuid = content["customer"]
        payment = content["payment_detail"]
        shipment = content["shipment_detail"]

        try:
            order = await self.aggregate.create_order(cart_uuid, customer_uuid, payment, shipment)
        except ValueError:
            raise ResponseException("An error occurred during order creation.")

        return Response(order)
