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
)
from uuid import (
    UUID,
)

from minos.common import (
    MinosConfig,
    MinosSetup,
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
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
)

metadata = MetaData()


product_table = Table(
    'product',
    metadata,
    Column("uuid", Text, primary_key=True),
    Column("version", Integer, nullable=False),
    Column("code", Text, nullable=False),
    Column("title", Text, nullable=False),
    Column("description", Text, nullable=False),
    Column("price", Numeric, nullable=False),
    Column("inventory_amount", Integer, nullable=False),
)


class ProductRepository(MinosSetup):
    """ProductInventory Repository class."""

    def __init__(self, database, host, port, user, password, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db_engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

        Session = sessionmaker(self.db_engine)
        session = Session()
        self.session = session

    async def _setup(self) -> NoReturn:
        product_table.create(self.db_engine, checkfirst=True)

    @classmethod
    def _from_config(cls, *args, config: MinosConfig, **kwargs) -> ProductRepository:
        return cls(*args, **(config.repository._asdict() | {"database": "product_query_db"}) | kwargs)

    async def get_without_stock(self) -> list[dict]:
        """Get product identifiers that do not have stock.

        :return: TODO.
        """
        return [row2dict(product) for product in self.session.query(Product).filter(Product.inventory_amount == 0)]

    async def get(self, uuid):
        """TODO

        :return: TODO
        """
        return product_table.select().where(product_table.c.uuid == uuid)

    async def create(self, uuid: UUID, version: int, inventory=None, **kwargs):
        """TODO

        :param uuid: TODO
        :param version: TODO
        :param inventory: TODO
        :param kwargs: TODO
        :return: TODO
        """
        if isinstance(uuid, UUID):
            uuid = str(uuid)
        if inventory is not None:
            kwargs["inventory_amount"] = inventory["amount"]

        op = product_table.insert(uuid=uuid, version=version, **kwargs)
        self.session.execute(op)

    async def update(self, uuid: UUID, version: int, inventory=None, **kwargs):
        """TODO

        :param uuid: TODO
        :param version: TODO
        :param inventory: TODO
        :param kwargs: TODO
        :return: TODO
        """
        if isinstance(uuid, UUID):
            uuid = str(uuid)
        if inventory is not None:
            kwargs["inventory_amount"] = inventory["amount"]

        op = product_table.update().where(product_table.c.uuid == uuid).values((kwargs | {"version": version}))
        self.session.execute(op)

    async def delete(self, uuid: UUID) -> NoReturn:
        """Delete an entry from the database.

        :param uuid: The product identifier.
        :return: This method does not return anything.
        """
        op = product_table.delete().where(product_table.c.uuid == uuid)
        self.session.execute(op)


def row2dict(row):
    """TODO

    :param row: TODO
    :return: TODO
    """
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d
