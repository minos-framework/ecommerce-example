from minos.cqrs import (
    CommandService,
)
from minos.networks import (
    Request,
    Response,
    enroute,
)


class PaymentCommandService(CommandService):
    """Payment Command Service class"""

    @enroute.rest.command("/payments", "POST")
    @enroute.broker.command("CreatePayment")
    async def create_payment(self, request: Request) -> Response:
        """Create a payment.

        :param request: A request instance containing the information to build a payment instance.
        :return: A response containing the newly created payment instance.
        """
        content = await request.content()
        credit_number = content["credit_number"]
        amount = content["amount"]
        payment = await self.aggregate.create_payment(credit_number, amount)
        return Response(payment)
