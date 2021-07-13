"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import (
    NoReturn,
)

from minos.common import (
    AggregateDiff,
    Event,
    Service,
)

# from minos.networks import (
#     subscribe,
# )
# from minos.saga import Saga, SagaContext
#
#
# def event_handler(event: Event):
#
#     async def _fn(context: SagaContext):
#         products = context["products"]
#         ticket = context["ticket"]
#
#         diff = context["diff"]
#         diff.products= products
#         diff.ticket = ticket
#
#         await OrderQueryService().order_created(diff)
#
#     saga = (
#         Saga("OrderCreated")
#         .step()
#         .invoke_participant("GetProducts", lambda c: c)
#         .on_reply("products")
#         .step()
#         .invoke_participant("GetTicket", lambda c: c)
#         .on_reply("ticket")
#         .commit(_fn)
#     )
#
#     await saga_manager.run(saga, SagaContext(event))


class OrderQueryService(Service):
    """TODO"""

    # @subscribe("OrderAdded")
    async def order_created(self, topic: str, event: Event) -> NoReturn:
        """TODO

        :param topic: TODO
        :param event: TODO
        :return: TODO
        """
        diff = event.data
        print(topic, diff)

    # @subscribe("OrderUpdated")
    async def order_updated(self, topic: str, event: Event) -> NoReturn:
        """TODO

        :param topic: TODO
        :param event: TODO
        :return: TODO
        """
        diff = event.data
        print(topic, diff)

    # @subscribe("OrderDeleted")
    async def order_deleted(self, topic: str, event: Event) -> NoReturn:
        """TODO

        :param topic: TODO
        :param event: TODO
        :return: TODO
        """
        diff = event.data
        print(topic, diff)
