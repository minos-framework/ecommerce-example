from __future__ import (
    annotations,
)

from minos.aggregate import (
    Condition,
    ExternalEntity,
    Ref,
    RootEntity,
)


class Credentials(RootEntity):
    """Credentials RootEntity class.

    The purpose of this aggregate is to store the needed information to be authenticated.
    """

    username: str
    password: str
    active: bool
    user: Ref[Customer]

    @classmethod
    async def exists_username(cls, username: str) -> bool:
        """Check if username already exists.

        :param username: The username to be checked.
        :return: ``True`` if the username exists or ``False`` otherwise.
        """
        try:
            await cls.find(Condition.EQUAL("username", username)).__anext__()
            return True
        except StopAsyncIteration:
            return False


class Customer(ExternalEntity):
    """Customer ExternalEntity class."""
