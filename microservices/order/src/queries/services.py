"""src.queries.services module."""

from minos.cqrs import QueryService
from minos.networks import (
    Request,
    enroute,
)


class OrderQueryService(QueryService):
    """Order Query Service class."""

    @enroute.broker.event("OrderCreated")
    async def order_created(self, request: Request) -> None:
        """Handle the order creation events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        print(await request.content())

    @enroute.broker.event("OrderUpdated")
    async def order_updated(self, request: Request) -> None:
        """Handle the order update events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        print(await request.content())

    @enroute.broker.event("OrderDeleted")
    async def order_deleted(self, request: Request) -> None:
        """Handle the order deletion events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        print(await request.content())
