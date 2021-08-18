"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from __future__ import annotations

from typing import NoReturn
from uuid import UUID

from minos.common import (
    FieldDiff,
    MinosConfig,
    MinosSetup,
)
from sqlalchemy import create_engine

from .models import (
    META,
    REVIEW_TABLE,
    ProductDTO,
)


class ReviewQueryRepository(MinosSetup):
    """ProductInventory Repository class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = create_engine("postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(**kwargs))

    async def _setup(self) -> NoReturn:
        META.create_all(self.engine)

    @classmethod
    def _from_config(cls, *args, config: MinosConfig, **kwargs) -> ReviewQueryRepository:
        return cls(*args, **(config.repository._asdict() | {"database": "review_query_db"}) | kwargs)

    async def create(self, **kwargs) -> NoReturn:
        """Create a new row.

        :param kwargs: The parameters of the creation query.
        :return: This method does not return anything.
        """
        kwargs = {k: v if not isinstance(v, FieldDiff) else v.value for k, v in kwargs.items()}

        kwargs["inventory_amount"] = kwargs["inventory"]["amount"]
        kwargs["inventory_reserved"] = kwargs["inventory"]["reserved"]
        kwargs["inventory_sold"] = kwargs["inventory"]["sold"]

        kwargs.pop("inventory")

        query = REVIEW_TABLE.insert().values(**kwargs)
        self.engine.execute(query)

    async def update(self, uuid: UUID, **kwargs) -> NoReturn:
        """Update an existing row.

        :param uuid: The identifier of the row.
        :param kwargs: The parameters to be updated.
        :return: This method does not return anything.
        """
        kwargs = {k: v if not isinstance(v, FieldDiff) else v.value for k, v in kwargs.items()}

        if "inventory" in kwargs:
            kwargs["inventory_amount"] = kwargs["inventory"]["amount"]
            kwargs["inventory_reserved"] = kwargs["inventory"]["reserved"]
            kwargs["inventory_sold"] = kwargs["inventory"]["sold"]

            kwargs.pop("inventory")

        query = REVIEW_TABLE.update().where(REVIEW_TABLE.columns.uuid == uuid).values(**kwargs)
        self.engine.execute(query)

    async def delete(self, uuid: UUID) -> NoReturn:
        """Delete an entry from the database.

        :param uuid: The product identifier.
        :return: This method does not return anything.
        """
        query = REVIEW_TABLE.delete().where(REVIEW_TABLE.columns.uuid == uuid)
        self.engine.execute(query)
