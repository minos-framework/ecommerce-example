from dependency_injector.wiring import (
    Provide,
)
from minos.aggregate import (
    AggregateDiff,
)
from minos.cqrs import (
    QueryService,
)
from minos.networks import (
    Request,
    enroute,
)

from .repositories import (
    PaymentAmountRepository,
)


class PaymentQueryService(QueryService):
    """Payment Query Service class"""

    repository: PaymentAmountRepository = Provide["payment_amount_repository"]

    @enroute.broker.event("PaymentCreated")
    @enroute.broker.event("PaymentUpdated")
    async def payment_created_or_updated(self, request: Request) -> None:
        """Handle the payment create events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        uuid = diff.uuid
        amount = diff["amount"]

        await self.repository.insert_payment_amount(uuid, amount)

    @enroute.broker.event("PaymentDeleted")
    async def payment_deleted(self, request: Request) -> None:
        """Handle the payment delete events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

        await self.repository.delete(diff.uuid)
