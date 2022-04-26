from __future__ import (
    annotations,
)

from asyncio import (
    gather,
)
from typing import (
    Any,
    Optional,
)
from uuid import (
    UUID,
)

from minos.aggregate import (
    Aggregate,
    ExternalEntity,
    Ref,
    RootEntity,
)


class Review(RootEntity):
    """Product Review class."""

    product: Ref[Product]
    user: Ref[Customer]
    title: str
    description: str
    score: int

    @staticmethod
    def validate_score(score: int) -> bool:
        if not isinstance(score, int):
            return False
        return 1 <= score <= 5


class Product(ExternalEntity):
    """Product ExternalEntity class."""

    title: str


class Customer(ExternalEntity):
    """Customer ExternalEntity class."""

    name: str


class ReviewAggregate(Aggregate[Review]):
    """Review Aggregate class."""

    async def create_review(self, product: UUID, user: UUID, title: str, description: str, score: int) -> Review:
        """TODO"""
        review, _ = await self.repository.create(
            Review, product=product, user=user, title=title, description=description, score=score,
        )
        return review

    async def update_review(self, uuid: UUID, content: dict[str, Any]) -> Review:
        """TODO"""
        review = await self.repository.get(Review, uuid)

        kwargs = dict(content)
        kwargs.pop("uuid")
        await self.repository.update(review, **kwargs)

        return review
