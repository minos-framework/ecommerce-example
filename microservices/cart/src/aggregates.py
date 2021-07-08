"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import (
    Union,
)

from minos.common import (
    Aggregate,
    DeclarativeModel,
)


class CartItem(DeclarativeModel):
    """Cart Aggregate class."""

    quantity: int
    product: int


class Cart(Aggregate):
    """Cart Aggregate class."""

    user: int
    products: list[Union[CartItem, None]]
