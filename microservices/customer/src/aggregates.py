from datetime import (
    datetime,
)

from minos.aggregate import (
    RootEntity,
    ValueObject,
)
from minos.aggregate import Aggregate


class Address(ValueObject):
    street: str
    street_no: int


class Customer(RootEntity):
    """Customer RootEntity class."""

    name: str
    surname: str
    address: Address
    created_at: datetime
    updated_at: datetime


class CustomerAggregate(Aggregate[Customer]):
    """Customer Aggregate class."""
