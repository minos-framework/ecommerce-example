"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import (
    Callable, NoReturn,
)

from minos.common import (
    AggregateDiff,
    Event,
)
from minos.cqrs import QueryService


def subscribe(func: Callable):
    async def wrapper(self, *args, **kwargs) -> NoReturn:
        if isinstance(args[0], AggregateDiff):
            return await func(self, *args, **kwargs)
        else:
            event = args[1]
            return await self._handle(event.data, func)

    return wrapper


class OrderQueryService(QueryService):
    """TODO"""

    @subscribe
    async def order_created(self, diff: AggregateDiff) -> NoReturn:
        """TODO

        :param diff: TODO
        :return: TODO
        """
        print(diff)

    @subscribe
    async def order_updated(self, diff: AggregateDiff) -> NoReturn:
        """TODO

        :param diff: TODO
        :return: TODO
        """
        print(diff)

    @subscribe
    async def order_deleted(self, diff: AggregateDiff) -> NoReturn:
        """TODO

        :param diff: TODO
        :return: TODO
        """
        print(diff)
