from sqlalchemy import (
    Boolean,
    Column,
    MetaData,
    String,
    Table,
)

META = MetaData()
USER_TABLE = Table(
    "users",
    META,
    Column("username", String(32), nullable=False),
    Column("password", String(32), nullable=False),
    Column("active", Boolean),
)
