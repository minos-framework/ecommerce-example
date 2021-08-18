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
REVIEW_TABLE = Table(
    "review",
    META,
    Column("product_uuid", UUID_PG(as_uuid=True), primary_key=True),
    Column("user_uuid", UUID_PG(as_uuid=True), primary_key=True),
    Column("version", Integer, nullable=False),
    Column("title", Text, nullable=False),
    Column("description", Text, nullable=False),
    Column("score", Integer, nullable=False),
    Column("product_title", Text, nullable=False),
    Column("username", Text, nullable=False),
)

ProductDTO = ModelType.build(
    "ProductDTO", {"product_uuid": UUID, "user_uuid": UUID, "title": str, "description": str, "score": int,
                   "product_title": str, "username": str}
)
