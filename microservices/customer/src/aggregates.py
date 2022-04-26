from datetime import datetime
from typing import (
    Any,
    Union,
)
from uuid import UUID

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

    async def create_customer(self, name: str, surname: str, address: Union[dict[str, Any], Address]) -> Customer:
        """TODO"""
        if not isinstance(address, Address):
            address = Address(**address)
        customer, _ = await self.repository.create(Customer, name, surname, address)
        return customer

    async def delete_customer(self, uuid: UUID) -> None:
        """TODO"""
        customer = await self.repository.get(Customer, uuid)
        await self.repository.delete(customer)
