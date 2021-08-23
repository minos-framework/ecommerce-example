from __future__ import annotations

from minos.common import Aggregate


class User(Aggregate):
    username: str
    password: str
    active: bool
