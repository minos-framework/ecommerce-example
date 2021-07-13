"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import (
    NoReturn,
)

from minos.common import (
    Event,
    Service,
)


class TicketQueryService(Service):
    """TODO"""

    # @subscribe("TicketAdded")
    async def ticket_created(self, topic: str, event: Event) -> NoReturn:
        """TODO

        :param topic: TODO
        :param event: TODO
        :return: TODO
        """
        diff = event.data
        print(topic, diff)

    # @subscribe("TicketUpdated")
    async def ticket_updated(self, topic: str, event: Event) -> NoReturn:
        """TODO

        :param topic: TODO
        :param event: TODO
        :return: TODO
        """
        diff = event.data
        print(topic, diff)

    # @subscribe("TicketDeleted")
    async def ticket_deleted(self, topic: str, event: Event) -> NoReturn:
        """TODO

        :param topic: TODO
        :param event: TODO
        :return: TODO
        """
        diff = event.data
        print(topic, diff)
