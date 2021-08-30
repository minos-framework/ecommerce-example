from __future__ import (
    annotations,
)

from minos.common import (
    Aggregate,
    AggregateRef,
    ModelRef
)


class User(AggregateRef):
    pass


class Credential(Aggregate):
    username: str
    password: str
    active: bool
    user = ModelRef[User]
