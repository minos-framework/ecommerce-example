"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from __future__ import (
    annotations,
)

from typing import (
    NoReturn,
    Optional,
)
from uuid import (
    UUID,
)

from aiopg.sa import (
    SAConnection,
)
from aiopg.sa.engine import (
    get_dialect,
)
from minos.common import (
    MinosConfig,
    PostgreSqlMinosDatabase,
    PostgreSqlPool,
)
from sqlalchemy import (
    create_engine,
)

from .models import (
    META,
    PRODUCT_TABLE,
    ProductDTO,
)


class ProductQueryRepository(PostgreSqlMinosDatabase):
    """ProductInventory Repository class."""

    _pool: Optional[PostgreSqlPool] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def _setup(self) -> NoReturn:
        await super()._setup()
        url = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        META.create_all(create_engine(url))

    @classmethod
    def _from_config(cls, *args, config: MinosConfig, **kwargs) -> ProductQueryRepository:
        return cls(*args, **(config.repository._asdict() | {"database": "product_query_db"}) | kwargs)

    async def get_without_stock(self) -> list[ProductDTO]:
        """Get product identifiers that do not have stock.

        :return: a list of dto instances.
        """
        query = PRODUCT_TABLE.select().where(PRODUCT_TABLE.columns.inventory_amount == 0)
        result = await self._execute(query)
        return [ProductDTO(**row) async for row in result]

    async def create(self, **kwargs) -> NoReturn:
        """Create a new row.

        :param kwargs: The parameters of the creation query.
        :return: This method does not return anything.
        """
        kwargs["inventory_amount"] = kwargs.pop("inventory")["amount"]

        query = PRODUCT_TABLE.insert().values(**kwargs)
        await self._execute(query)

    async def update(self, uuid: UUID, **kwargs) -> NoReturn:
        """Update an existing row.

        :param uuid: The identifier of the row.
        :param kwargs: The parameters to be updated.
        :return: This method does not return anything.
        """
        if "inventory" in kwargs:
            kwargs["inventory_amount"] = kwargs.pop("inventory")["amount"]

        query = PRODUCT_TABLE.update().where(PRODUCT_TABLE.columns.uuid == uuid).values(**kwargs)
        await self._execute(query)

    async def delete(self, uuid: UUID) -> NoReturn:
        """Delete an entry from the database.

        :param uuid: The product identifier.
        :return: This method does not return anything.
        """
        query = PRODUCT_TABLE.delete().where(PRODUCT_TABLE.columns.uuid == uuid)
        await self._execute(query)

    async def _execute(self, query):
        async with self.pool.acquire() as conn:
            return await SAConnection(conn, _ENGINE).execute(query)


class _Engine:
    dialect = get_dialect()

    async def release(self, *args, **kwargs):
        """TODO"""


_ENGINE = _Engine()
