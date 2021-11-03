from __future__ import (
    annotations,
)

from uuid import (
    UUID,
)

from minos.common import (
    FieldDiff,
    MinosConfig,
    MinosSetup,
)
from sqlalchemy import (
    create_engine,
)
from sqlalchemy.orm import (
    sessionmaker,
)

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

    async def _setup(self) -> None:
        META.create_all(self.engine)

    @classmethod
    def _from_config(cls, *args, config: MinosConfig, **kwargs) -> OrderQueryRepository:
        return cls(*args, **(config.repository._asdict() | {"database": "order_query_db"}) | kwargs)

    async def create(self, **kwargs) -> None:
        """Create a new row.

        :param kwargs: The parameters of the creation query.
        :return: This method does not return anything.
        """
        kwargs = {k: v if not isinstance(v, FieldDiff) else v.value for k, v in kwargs.items()}

        kwargs["ticket_uuid"] = kwargs["ticket"]["uuid"]
        kwargs["payment_uuid"] = kwargs["payment"]["uuid"]
        kwargs["customer_uuid"] = kwargs["customer"]["uuid"]
        kwargs["payment_detail"] = dict(kwargs["payment_detail"])
        kwargs["shipment_detail"] = dict(kwargs["shipment_detail"])

        kwargs.pop("payment")
        kwargs.pop("ticket")
        kwargs.pop("customer")

        query = ORDER_TABLE.insert().values(**kwargs)
        self.engine.execute(query)

    async def get(self, uuid: UUID) -> None:
        """Create a new row.

        :param uuid: The parameters of the creation query.
        :return: This method does not return anything.
        """

        query = ORDER_TABLE.select().where(ORDER_TABLE.columns.uuid == uuid)
        res = self.engine.execute(query)

        order = None
        for row in res:
            order = OrderDTO(**row)

        return order

    async def get_by_user(self, uuid: UUID) -> list[OrderDTO]:
        """Create a new row.

        :param uuid: The parameters of the creation query.
        :return: This method does not return anything.
        """

        query = ORDER_TABLE.select().where(ORDER_TABLE.columns.customer_uuid == uuid)
        res = self.engine.execute(query)

        orders = [OrderDTO(**row) for row in res]

        return orders
