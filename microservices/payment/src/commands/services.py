"""src.commands.services module."""

from minos.cqrs import (
    CommandService,
)
from minos.networks import (
    Request,
    Response,
    enroute,
)

from ..aggregates import (
    Payment,
)


class PaymentCommandService(CommandService):
    """Payment Command Service class"""

    @staticmethod
    @enroute.rest.command("/payments", "POST")
    @enroute.broker.command("CreatePayment")
    async def create_payment(request: Request) -> Response:
        """Create a payment.

        :param request: A request instance containing the information to build a payment instance.
        :return: A response containing the newly created payment instance.
        """
        content = await request.content()
        credit_number = content["credit_number"]
        amount = content["amount"]
        status = "created"

        payment = await Payment.create(credit_number, amount, status)

        return Response(payment)
