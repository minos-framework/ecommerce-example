"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import (
    UUID,
)

from minos.common import (
    Service,
)
from minos.saga import (
    SagaContext,
)

from .aggregates import (
    User,
)


class UserService(Service):
    """Ticket Service class"""

    async def create_user(self, products: list[int]) -> UUID:
        """
        Creates a fake_payment_service

        :param products: List of `users`
        """
        return await self.saga_manager.run("CreateUser", context=SagaContext(product_ids=products))

    @staticmethod
    async def get_users(ids: list[int]) -> list[User]:
        """Get a list of tickets.

        :param ids: List of ticket identifiers.
        :return: A list of ``Ticket`` instances.
        """
        values = {v.id: v async for v in User.get(ids=ids)}
        return [values[id] for id in ids]
