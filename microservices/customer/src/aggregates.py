from datetime import (
    datetime,
)

from minos.aggregate import (
    Aggregate,
    ValueObject,
)


class Address(ValueObject):
    street: str
    street_no: int


class Customer(Aggregate):
    """Customer Aggregate class."""

    name: str
    surname: str
    address: Address
    created_at: datetime
    updated_at: datetime
