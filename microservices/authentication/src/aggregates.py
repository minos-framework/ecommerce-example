from __future__ import (
    annotations,
)

from minos.common import (
    Aggregate,
)


class Credential(Aggregate):
    username: str
    password: str
    active: bool
