"""
Copyright (C) 2021 Clariteia SL
This file is part of minos framework.
Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
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
TICKET_TABLE = Table(
    "ticket",
    META,
    Column("uuid", UUID_PG(as_uuid=True), primary_key=True),
    Column("version", Integer, nullable=False),
    Column("code", Text, nullable=False),
    Column("total_price", Numeric, nullable=False),
)
TICKET_ENTRY_TABLE = Table(
    "ticket_entries",
    META,
    Column("ticket_uuid", UUID_PG(as_uuid=True), primary_key=True),
    Column("title", Text, nullable=False),
    Column("unit_price", Numeric, nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("product_uuid", UUID_PG(as_uuid=True), nullable=False),
    ForeignKeyConstraint(["ticket_uuid"], ["ticket.uuid"], name="fk_ticket", ondelete="CASCADE",),
)
TicketEntryDTO = ModelType.build(
    "TicketEntryDTO", {"ticket_uuid": UUID, "title": str, "unit_price": float, "quantity": int, "product_uuid": UUID},
)
TicketDTO = ModelType.build(
    "TicketDTO", {"uuid": UUID, "version": int, "code": str, "total_price": float, "entries": list[TicketEntryDTO]}
)
