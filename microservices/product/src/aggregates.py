"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import (
    Aggregate,
)


class Product(Aggregate):
    """TODO"""

    code: str
    title: str
    description: str
    price: float
