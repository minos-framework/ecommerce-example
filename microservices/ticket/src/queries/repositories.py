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
    PostgreSqlMinosDatabase,
)
from sqlalchemy import (
    create_engine,
)
from sqlalchemy.orm import (
    sessionmaker,
)

from .models import (
    META,
    TICKET_ENTRY_TABLE,
    TICKET_TABLE,
    TicketDTO,
    TicketEntryDTO,
)


class TicketQueryRepository(PostgreSqlMinosDatabase):
    """Ticket Amount repository"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = create_engine("postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(**kwargs))
        self.session = sessionmaker(bind=self.engine)()

    async def _setup(self) -> NoReturn:
        META.create_all(self.engine)

    @classmethod
    def _from_config(cls, *args, config: MinosConfig, **kwargs) -> TicketQueryRepository:
        return cls(*args, **(config.repository._asdict() | {"database": "ticket_query_db"}) | kwargs)

    async def insert(self, uuid: UUID, version: int, code: str, total_price: float, entries) -> NoReturn:
        """Insert Payment amount
        :param uuid: UUID
        :param version: Version ID
        :param code: Ticket code
        :param total_price: Ticket total price
        :param entries: Ticket entries
        :return: Nothing
        """
        query = TICKET_TABLE.insert().values(uuid=uuid, version=version, code=code, total_price=total_price)
        self.engine.execute(query)

        for entry in entries:
            query = TICKET_ENTRY_TABLE.insert().values(
                ticket_uuid=uuid,
                title=entry.title,
                unit_price=entry.unit_price,
                quantity=entry.quantity,
                product_uuid=entry.product.uuid,
            )
            self.engine.execute(query)

    async def get_ticket(self, ticket_uuid: UUID) -> dict:
        """Insert Payment amount
        :param ticket_uuid: UUID
        :return: Nothing
        """
        result = {}

        try:
            ticket_query = self.session.query(TICKET_TABLE).filter(TICKET_TABLE.columns.uuid == ticket_uuid).one()
        except Exception:
            return {"error": "Invalid Ticket UUID"}

        try:
            ticket_entries_query = TICKET_ENTRY_TABLE.select().where(
                TICKET_ENTRY_TABLE.columns.ticket_uuid == ticket_uuid
            )
            ticket_entries_results = self.engine.execute(ticket_entries_query)
        except Exception:
            return {"error": "An error occurred while obtaining Ticket entries."}

        try:
            ticket_entries = [TicketEntryDTO(**row) for row in ticket_entries_results]

            result = TicketDTO(**ticket_query, entries=ticket_entries)
        except Exception:
            result = {"error": "An error occurred when formatting result."}

        return result
