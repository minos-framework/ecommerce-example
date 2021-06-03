"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import (
    MinosModel,
)


class ProductDto(MinosModel):
    id: int
    external_id: int
    name: str
    description: str
    brand: str
    unit_price: float


class ProductsQueryDto(MinosModel):
    ids: list[int]
