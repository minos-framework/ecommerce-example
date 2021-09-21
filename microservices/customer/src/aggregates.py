"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from datetime import (
    datetime,
)

from minos.common import (
    Aggregate,
    ValueObject,
)


class Address(ValueObject):
    street: str
    street_no: int


class Customer(Aggregate):
    """Customer Aggregate class."""

    name: str
    surname: str
    address: Address
    created_at: datetime
    updated_at: datetime
