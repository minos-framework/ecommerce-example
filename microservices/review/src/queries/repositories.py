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
from sqlalchemy import (
    asc,
    create_engine,
    desc,
    func,
)
from sqlalchemy.orm import sessionmaker

from .models import (
    META,
    REVIEW_TABLE,
    ReviewDTO,
    RatingDTO,
)


ORDER_ASC = "asc"
ORDER_DESC = "desc"


class ReviewQueryRepository(MinosSetup):
    """ProductInventory Repository class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = create_engine("postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(**kwargs))
        self.session = sessionmaker(bind=self.engine)()

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

        kwargs["product_uuid"] = kwargs["product"]["uuid"]
        kwargs["product_title"] = kwargs["product"]["title"]
        kwargs["user_uuid"] = kwargs["user"]["uuid"]
        kwargs["username"] = kwargs["user"]["username"]

        kwargs.pop("product")
        kwargs.pop("user")

        query = REVIEW_TABLE.insert().values(**kwargs)
        self.engine.execute(query)

    async def get_reviews_by_product(self, product: UUID) -> NoReturn:
        """Create a new row.

        :param kwargs: The parameters of the creation query.
        :return: This method does not return anything.
        """

        query = REVIEW_TABLE.select().where(REVIEW_TABLE.columns.product_uuid == product)
        res = self.engine.execute(query)

        reviews = [ReviewDTO(**row) for row in res]

        return reviews

    async def product_score(self, product: UUID, limit: int = 1, order: str = ORDER_ASC) -> NoReturn:
        """Create a new row.

        :param product: Product UUID.
        :param limit: Records quantity to return.
        :param order: Score order.
        :return: This method does not return anything.
        """
        direction = desc if order == ORDER_DESC else asc

        query = (
            REVIEW_TABLE.select()
            .where(REVIEW_TABLE.columns.product_uuid == product)
            .order_by(direction(REVIEW_TABLE.columns.score))
            .limit(limit)
        )
        res = self.engine.execute(query)

        reviews = [ReviewDTO(**row) for row in res]

        return reviews

    async def worst_product_rating(self, product: UUID) -> NoReturn:
        """Create a new row.

        :param kwargs: The parameters of the creation query.
        :return: This method does not return anything.
        """

        query = (
            REVIEW_TABLE.select()
            .where(REVIEW_TABLE.columns.product_uuid == product)
            .order_by(REVIEW_TABLE.columns.score.asc())
            .limit(1)
        )
        res = self.engine.execute(query)

        reviews = [ReviewDTO(**row) for row in res]

        return reviews

    async def get_reviews_by_user(self, user: UUID) -> NoReturn:
        """Create a new row.

        :param kwargs: The parameters of the creation query.
        :return: This method does not return anything.
        """

        query = REVIEW_TABLE.select().where(REVIEW_TABLE.columns.user_uuid == user)
        res = self.engine.execute(query)

        reviews = [ReviewDTO(**row) for row in res]

        return reviews

    async def reviews_score(self, limit: int = 10, order: str = ORDER_ASC) -> NoReturn:
        """Top 10 Most Rated Products.

        :param limit: Records quantity to return.
        :param order: Score order.
        :return: This method does not return anything.
        """
        direction = desc if order == ORDER_DESC else asc

        res = (
            self.session.query(
                REVIEW_TABLE.columns.product_uuid,
                REVIEW_TABLE.columns.product_title,
                func.avg(REVIEW_TABLE.columns.score).label("average"),
            )
            .group_by(REVIEW_TABLE.columns.product_uuid, REVIEW_TABLE.columns.product_title)
            .order_by(direction("average"))
            .limit(limit)
        )

        reviews = [RatingDTO(**row) for row in res]

        return reviews

    async def last_reviews(self, limit: int = 1) -> NoReturn:
        """Create a new row.

        :param limit: Records quantity.
        :return: This method does not return anything.
        """

        query = REVIEW_TABLE.select().order_by(desc(REVIEW_TABLE.columns.date)).limit(limit)

        res = self.engine.execute(query)

        reviews = [ReviewDTO(**row) for row in res]

        return reviews

    async def update(self, uuid: UUID, **kwargs) -> NoReturn:
        """Update an existing row.

        :param uuid: The identifier of the row.
        :param kwargs: The parameters to be updated.
        :return: This method does not return anything.
        """
        kwargs = {k: v if not isinstance(v, FieldDiff) else v.value for k, v in kwargs.items()}

        query = REVIEW_TABLE.update().where(REVIEW_TABLE.columns.uuid == uuid).values(**kwargs)
        self.engine.execute(query)

    async def delete(self, uuid: UUID) -> NoReturn:
        """Delete an entry from the database.

        :param uuid: The product identifier.
        :return: This method does not return anything.
        """
        query = REVIEW_TABLE.delete().where(REVIEW_TABLE.columns.uuid == uuid)
        self.engine.execute(query)
