import datetime
from typing import Any
from uuid import UUID

from minos.common import ModelType
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    Numeric,
    Table,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as UUID_PG

META = MetaData()
ORDER_TABLE = Table(
    "order",
    META,
    Column("uuid", UUID_PG(as_uuid=True), primary_key=True),
    Column("version", Integer, nullable=False),
    Column("ticket_uuid", UUID_PG(as_uuid=True)),
    Column("payment_uuid", UUID_PG(as_uuid=True)),
    Column("customer_uuid", UUID_PG(as_uuid=True)),
    Column("total_amount", Numeric, nullable=False),
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
        "customer_uuid": UUID,
        "total_amount": float,
        "payment_detail": dict[str, Any],
        "shipment_detail": dict[str, Any],
        "status": str,
        "created_at": datetime.datetime,
        "updated_at": datetime.datetime,
    },
)
