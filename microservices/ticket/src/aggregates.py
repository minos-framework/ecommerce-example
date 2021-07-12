"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import UUID

from minos.common import (
    Aggregate,
)


class Ticket(Aggregate):
    """Ticket Aggregate class."""

    code: str

    payments: list[UUID]
    total_price: float
