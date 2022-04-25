from __future__ import (
    annotations,
)

from typing import (
    Any,
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

    @staticmethod
    async def create_review(product: UUID, user: UUID, title: str, description: str, score: int) -> Review:
        """TODO"""
        review = await Review.create(product=product, user=user, title=title, description=description, score=score)
        return review

    @staticmethod
    async def update_review(uuid: UUID, content: dict[str, Any]) -> Review:
        """TODO"""
        review = await Review.get(uuid)

        kwargs = dict(content)
        kwargs.pop("uuid")
        await review.update(**kwargs)

        return review
