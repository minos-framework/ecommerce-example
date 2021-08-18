"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import (
    NoReturn,
)
from uuid import (
    UUID,
)

from dependency_injector.wiring import (
    Provide,
)
from minos.common import (
    UUID_REGEX,
    AggregateDiff,
    ModelType,
)
from minos.cqrs import (
    QueryService,
)
from minos.networks import (
    Request,
    Response,
    ResponseException,
    enroute,
)

from .repositories import (
    ReviewQueryRepository,
)


class ReviewQueryService(QueryService):
    """Product Query Service class."""

    repository: ReviewQueryRepository = Provide["review_repository"]





