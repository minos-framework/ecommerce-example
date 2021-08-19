from sqlalchemy import (
    Column,
    String,
    MetaData,
    Table,
    Boolean
)

META = MetaData()
USER_TABLE = Table(
    "users",
    META,
    Column("username", String(32), nullable=False),
    Column("password", String(32), nullable=False),
    Column("active", Boolean)
)
