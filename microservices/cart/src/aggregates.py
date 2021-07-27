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
    price: Union[float, int, None]


class Cart(Aggregate):
    """Cart Aggregate class."""

    user: int
    products: list[Union[CartItem, None]]


"""
class Product(SubAggregate):
    id: int
    title: str
    price: float


class CartItem(DeclarativeModel):

    quantity: int
    product: ModelRef[Product]
    price: Union[float, int, None]


class Cart(Aggregate):

    user: int
    products: list[Union[CartItem, None]]
"""