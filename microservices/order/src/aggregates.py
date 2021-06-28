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
)


class Order(Aggregate):
    """TODO"""

    products: list[int]
    ticket: int
    status: str

    created_at: datetime
    updated_at: datetime
