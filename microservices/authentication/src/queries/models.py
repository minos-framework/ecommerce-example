from sqlalchemy import (
    Boolean,
    Column,
    MetaData,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID as UUID_PG

META = MetaData()
CREDENTIALS_TABLE = Table(
    "credentials",
    META,
    Column("uuid", UUID_PG(as_uuid=True), primary_key=True),
    Column("username", String(32), unique=True, nullable=False),
    Column("password", String(32), nullable=False),
    Column("active", Boolean),
    Column("user", UUID_PG(as_uuid=True)),
)
