"""
Copyright (C) 2021 Clariteia SL
This file is part of minos framework.
Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import (
    Any,
    Union,
)
from uuid import UUID

from minos.common import ModelType
from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    Numeric,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as UUID_PG
from sqlalchemy.schema import ForeignKeyConstraint

META = MetaData()
CART_TABLE = Table(
    "cart",
    META,
    Column("uuid", UUID_PG(as_uuid=True), primary_key=True),
    Column("version", Integer, nullable=False),
    Column("user_id", Integer, nullable=False),
)
CART_ITEM_TABLE = Table(
    "cart_items",
    META,
    Column("product_id", UUID_PG(as_uuid=True), primary_key=True),
    Column("cart_id", UUID_PG(as_uuid=True), primary_key=True),
    Column("quantity", Integer, nullable=False),
    Column("title", Text, nullable=False),
    Column("description", Text, nullable=False),
    Column("price", Numeric, nullable=False),
    ForeignKeyConstraint(["cart_id"], ["cart.uuid"], name="fk_cart", ondelete="CASCADE",),
)
CartItemDTO = ModelType.build(
    "CartItemDTO",
    {"product_id": UUID, "cart_id": UUID, "quantity": int, "title": str, "description": str, "price": float},
)
CartDTO = ModelType.build("CartDTO", {"uuid": UUID, "version": int, "products": list[CartItemDTO]})
