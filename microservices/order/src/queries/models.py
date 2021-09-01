"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
import datetime
from uuid import UUID

from minos.common import ModelType
from sqlalchemy import (
    Column,
    MetaData,
    Table,
    Text,
    text,
    DateTime,
    Integer,
)
from sqlalchemy.dialects.postgresql import (
    UUID as UUID_PG,
    JSONB,
)

META = MetaData()
ORDER_TABLE = Table(
    "order",
    META,
    Column("uuid", UUID_PG(as_uuid=True), primary_key=True),
    Column("version", Integer, nullable=False),
    Column("ticket_uuid", UUID_PG(as_uuid=True)),
    Column("payment_uuid", UUID_PG(as_uuid=True)),
    Column("user_uuid", UUID_PG(as_uuid=True)),
    Column("payment_detail", JSONB, default=text("'{}'::jsonb"), server_default=text("'{}'::jsonb")),
    Column("shipment_detail", JSONB, default=text("'{}'::jsonb"), server_default=text("'{}'::jsonb")),
    Column("status", Text, nullable=False),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
)

OrderDTO = ModelType.build(
    "OrderDTO",
    {
        "uuid": UUID,
        "ticket_uuid": UUID,
        "payment_uuid": UUID,
        "user_uuid": UUID,
        "payment_detail": dict,
        "shipment_detail": dict,
        "status": str,
        "created_at": datetime.datetime,
        "updated_at": datetime.datetime,
    },
)
