from __future__ import annotations

from minos.common import (
    Aggregate,
    AggregateRef,
    ModelRef,
)


class Customer(AggregateRef):
    pass


class Credentials(Aggregate):
    username: str
    password: str
    active: bool
    user = ModelRef[Customer]
