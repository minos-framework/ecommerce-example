from datetime import (
    datetime,
)
from typing import (
    Any,
    Union,
)
from uuid import (
    UUID,
)

from minos.aggregate import (
    Aggregate,
    RootEntity,
    ValueObject,
)


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

    @staticmethod
    async def create_customer(name: str, surname: str, address: Union[dict[str, Any], Address]) -> Customer:
        """TODO"""
        if not isinstance(address, Address):
            address = Address(**address)
        customer = await Customer.create(name, surname, address)
        return customer

    @staticmethod
    async def delete_customer(uuid: UUID) -> None:
        """TODO"""
        customer = await Customer.get(uuid)
        await customer.delete()
