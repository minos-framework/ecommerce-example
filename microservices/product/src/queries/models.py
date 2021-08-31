"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import (
    UUID,
)

from minos.common import (
    ModelType,
)
from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    Numeric,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as UUID_PG

META = MetaData()
PRODUCT_TABLE = Table(
    "product",
    META,
    Column("uuid", UUID_PG(as_uuid=True), primary_key=True),
    Column("version", Integer, nullable=False),
    Column("code", Text, nullable=False),
    Column("title", Text, nullable=False),
    Column("description", Text, nullable=False),
    Column("price", Numeric, nullable=False),
    Column("reviews_count", Integer, default=0),
    Column("reviews_score", Numeric, default=0),
    Column("inventory_amount", Integer, nullable=False),
    Column("inventory_reserved", Integer, nullable=False),
    Column("inventory_sold", Integer, nullable=False),
)

ProductDTO = ModelType.build(
    "ProductDTO",
    {
        "uuid": UUID,
        "code": str,
        "title": str,
        "description": str,
        "price": float,
        "reviews_count": int,
        "reviews_score": float,
    },
)
