"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from __future__ import annotations
from typing import Optional
from uuid import uuid4

from minos.common import (
    Aggregate,
    AggregateRef,
    ModelRef,
)


class Review(Aggregate):
    """Product Review class."""

    product: ModelRef[Product]
    user: ModelRef[User]
    title: str
    description: str
    score: int

    @staticmethod
    def validate_score(score: int) -> bool:
        if not isinstance(score, int):
            return False
        return 1 <= score <= 5


class Product(AggregateRef):
    """Product AggregateRef class."""

    title: str


class User(AggregateRef):
    """User AggregateRef class."""

    username: str
