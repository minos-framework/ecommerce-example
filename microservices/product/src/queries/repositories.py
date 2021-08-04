"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from __future__ import annotations

from typing import NoReturn
from uuid import UUID

from minos.common import (
    MinosConfig,
    MinosSetup,
    ModelType,
)
from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    Numeric,
    Table,
    Text,
    create_engine,
)
from sqlalchemy.dialects.postgresql import UUID as UUID_PG

metadata = MetaData()

PRODUCT_TABLE = Table(
    "product",
    metadata,
    Column("uuid", UUID_PG(as_uuid=True), primary_key=True),
    Column("version", Integer, nullable=False),
    Column("code", Text, nullable=False),
    Column("title", Text, nullable=False),
    Column("description", Text, nullable=False),
    Column("price", Numeric, nullable=False),
    Column("inventory_amount", Integer, nullable=False),
)
ProductDTO = ModelType.build("Product", {"uuid": UUID, "code": str, "title": str, "description": str, "price": float})


class ProductQueryRepository(MinosSetup):
    """ProductInventory Repository class."""

    def __init__(self, database: str, host: str, port: int, user: str, password: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

    async def _setup(self) -> NoReturn:
        PRODUCT_TABLE.create(self.engine, checkfirst=True)

    @classmethod
    def _from_config(cls, *args, config: MinosConfig, **kwargs) -> ProductQueryRepository:
        return cls(*args, **(config.repository._asdict() | {"database": "product_query_db"}) | kwargs)

    async def get_without_stock(self) -> list[ProductDTO]:
        """Get product identifiers that do not have stock.

        :return: a list of dto instances.
        """
        query = PRODUCT_TABLE.select().where(PRODUCT_TABLE.columns.inventory_amount == 0)
        result = self._execute(query)
        return [ProductDTO(**row) for row in result]

    async def create(self, **kwargs) -> NoReturn:
        """Create a new row.

        :param kwargs: The parameters of the creation query.
        :return: This method does not return anything.
        """
        kwargs["inventory_amount"] = kwargs.pop("inventory")["amount"]

        query = PRODUCT_TABLE.insert().values(**kwargs)
        self._execute(query)

    async def update(self, uuid: UUID, **kwargs) -> NoReturn:
        """Update an existing row.

        :param uuid: The identifier of the row.
        :param kwargs: The parameters to be updated.
        :return: This method does not return anything.
        """
        kwargs["inventory_amount"] = kwargs.pop("inventory")["amount"]

        query = PRODUCT_TABLE.update().where(PRODUCT_TABLE.columns.uuid == uuid).values(**kwargs)
        self._execute(query)

    async def delete(self, uuid: UUID) -> NoReturn:
        """Delete an entry from the database.

        :param uuid: The product identifier.
        :return: This method does not return anything.
        """
        self._execute(PRODUCT_TABLE.delete().where(PRODUCT_TABLE.columns.uuid == uuid))

    def _execute(self, op):
        return self.engine.execute(op)
