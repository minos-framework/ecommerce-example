"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from __future__ import (
    annotations,
)

from datetime import (
    datetime,
)
from typing import (
    Optional,
)

from minos.common import (
    Aggregate,
    ValueObject,
    ValueObjectSet,
)


class Address(ValueObject):
    street: str
    street_no: int


class User(Aggregate):
    """User Aggregate class."""

    username: str
    password: str
    status: str
    address: Address
    created_at: datetime

    credit_cards: ValueObjectSet[CreditCard]


class CreditCard(ValueObject):
    """TODO"""

    name: str
