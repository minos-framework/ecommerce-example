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
    ORDER_TABLE,
    OrderDTO,
)

ORDER_ASC = "asc"
ORDER_DESC = "desc"


class OrderQueryRepository(MinosSetup):
    """ProductInventory Repository class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = create_engine("postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(**kwargs))
        self.session = sessionmaker(bind=self.engine)()

    async def _setup(self) -> NoReturn:
        META.create_all(self.engine)

    @classmethod
    def _from_config(cls, *args, config: MinosConfig, **kwargs) -> OrderQueryRepository:
        return cls(*args, **(config.repository._asdict() | {"database": "order_query_db"}) | kwargs)

    async def create(self, **kwargs) -> NoReturn:
        """Create a new row.

        :param kwargs: The parameters of the creation query.
        :return: This method does not return anything.
        """
        kwargs = {k: v if not isinstance(v, FieldDiff) else v.value for k, v in kwargs.items()}

        kwargs["ticket_uuid"] = kwargs["ticket"]
        kwargs["payment_uuid"] = kwargs["payment"]
        kwargs["user_uuid"] = kwargs["user"]["uuid"]
        kwargs["payment_detail"] = dict(kwargs["payment_detail"])
        kwargs["shipment_detail"] = dict(kwargs["shipment_detail"])

        kwargs.pop("payment")
        kwargs.pop("ticket")
        kwargs.pop("user")

        query = ORDER_TABLE.insert().values(**kwargs)
        self.engine.execute(query)
