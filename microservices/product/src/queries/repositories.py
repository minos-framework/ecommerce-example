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
    Numeric,
    Text,
    create_engine,
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
)

Base = declarative_base()


class Product(Base):
    """TODO"""

    __tablename__ = "product"

    uuid = Column(Text, primary_key=True)
    version = Column("version", Integer, nullable=False)
    code = Column("code", Text, nullable=False)
    title = Column("title", Text, nullable=False)
    description = Column("description", Text, nullable=False)
    price = Column("price", Numeric, nullable=False)
    inventory_amount = Column("inventory_amount", Integer, nullable=False)


class ProductRepository(MinosSetup):
    """ProductInventory Repository class."""

    def __init__(self, database, host, port, user, password, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db_engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

        Session = sessionmaker(self.db_engine)
        session = Session()
        self.session = session

    async def _setup(self) -> NoReturn:
        Base.metadata.create_all(self.db_engine, Base.metadata.tables.values(), checkfirst=True)

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

        return self.session.query(Product).get(uuid)

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

        product = Product(uuid=uuid, version=version, **kwargs)
        self.session.add(product)
        self.session.commit()

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

        product = self.session.query(Product).get(uuid)
        for k, v in (kwargs | {"version": version}).items():
            setattr(product, k, v)
        self.session.commit()

    async def delete(self, uuid: UUID) -> NoReturn:
        """Delete an entry from the database.

        :param uuid: The product identifier.
        :return: This method does not return anything.
        """
        product = self.session.query(Product).get(uuid)
        self.session.delete(product)
        self.session.commit()


def row2dict(row):
    """TODO

    :param row: TODO
    :return: TODO
    """
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d
