"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from datetime import (
    datetime,
)
from uuid import (
    UUID,
)

from minos.common import (
    Aggregate,
)


class Order(Aggregate):
    """Order Aggregate class."""

    products: list[UUID]
    ticket: UUID
    status: str

    created_at: datetime
    updated_at: datetime
