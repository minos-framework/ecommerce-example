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
    Entity,
    ValueObject,
)


class Address(ValueObject):
    """Address Value Object class."""

    street: str
    street_no: int


class Customer(Entity):
    """Customer Entity class."""

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

        customer, delta = await self.repository.create(Customer, name, surname, address)
        await self.publish_domain_event(delta)

        return customer

    async def delete_customer(self, uuid: UUID) -> None:
        """TODO"""
        customer = await self.repository.get(Customer, uuid)
        delta = await self.repository.delete(customer)
        await self.publish_domain_event(delta)
