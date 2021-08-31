from __future__ import (
    annotations,
)

from minos.common import (
    Aggregate,
)


class Credentials(Aggregate):
    username: str
    password: str
    active: bool
