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


class PaymentQueryService(Service):
    """TODO"""

    # @subscribe("PaymentAdded")
    async def payment_created(self, topic: str, event: Event) -> NoReturn:
        """TODO

        :param topic: TODO
        :param event: TODO
        :return: TODO
        """
        diff = event.data
        print(topic, diff)

    # @subscribe("PaymentUpdated")
    async def payment_updated(self, topic: str, event: Event) -> NoReturn:
        """TODO

        :param topic: TODO
        :param event: TODO
        :return: TODO
        """
        diff = event.data
        print(topic, diff)

    # @subscribe("PaymentDeleted")
    async def payment_deleted(self, topic: str, event: Event) -> NoReturn:
        """TODO

        :param topic: TODO
        :param event: TODO
        :return: TODO
        """
        diff = event.data
        print(topic, diff)
