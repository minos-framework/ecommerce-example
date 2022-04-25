from minos.aggregate import (
    Event,
)
from minos.common import (
    Inject,
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

    @Inject()
    def __init__(self, repository: PaymentAmountRepository, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = repository

    @enroute.broker.event("PaymentCreated")
    @enroute.broker.event("PaymentUpdated")
    async def payment_created_or_updated(self, request: Request) -> None:
        """Handle the payment create events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: Event = await request.content()
        uuid = diff.uuid
        amount = diff["amount"]

        await self.repository.insert_payment_amount(uuid, amount)

    @enroute.broker.event("PaymentDeleted")
    async def payment_deleted(self, request: Request) -> None:
        """Handle the payment delete events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: Event = await request.content()

        await self.repository.delete(diff.uuid)
