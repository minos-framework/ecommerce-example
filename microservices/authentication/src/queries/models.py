from sqlalchemy import (
    Column,
    String,
    MetaData,
    Table,
    Boolean
)
from sqlalchemy.dialects.postgresql import UUID as UUID_PG

META = MetaData()
USER_TABLE = Table(
    "users",
    META,
    Column("username", String(32), nullable=False),
    Column("password", String(32), nullable=False),
    Column("active", Boolean)
)
