"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from __future__ import (
    annotations,
)

from typing import (
    Optional,
)

from minos.common import (
    Aggregate,
    AggregateRef,
    Entity,
    EntitySet,
    ModelRef,
    ValueObject,
)


class Inventory(ValueObject):
    """Inventory Object Value class."""

    amount: int


class Product(Aggregate):
    """Product class."""

    code: str
    title: str
    description: str
    price: float

    inventory: Inventory

    reviews: EntitySet[Review]


class Review(Entity):
    """TODO"""

    stars: float
    message: str


#     user: ModelRef[User]
#
#
# class User(AggregateRef):
#     """TODO"""
#
#     username: str
