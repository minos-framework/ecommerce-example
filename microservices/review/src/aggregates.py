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
    Entity,
    Ref,
)


# noinspection PyUnresolvedReferences
class Review(Entity):
    """Product Review Entity class."""

    product: Ref["Product"]
    user: Ref["Customer"]
    title: str
    description: str
    score: int

    @staticmethod
    def validate_score(score: int) -> bool:
        if not isinstance(score, int):
            return False
        return 1 <= score <= 5


class ReviewAggregate(Aggregate[Review]):
    """Review Aggregate class."""

    async def create_review(self, product: UUID, user: UUID, title: str, description: str, score: int) -> Review:
        """TODO"""
        review, delta = await self.repository.create(
            Review, product=product, user=user, title=title, description=description, score=score,
        )
        await self.publish_domain_event(delta)

        return review

    async def update_review(self, uuid: UUID, content: dict[str, Any]) -> Review:
        """TODO"""
        review = await self.repository.get(Review, uuid)

        kwargs = dict(content)
        kwargs.pop("uuid")

        _, delta = await self.repository.update(review, **kwargs)
        await self.publish_domain_event(delta)

        return review
