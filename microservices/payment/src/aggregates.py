from minos.aggregate import RootEntity


class Payment(RootEntity):
    """Payment RootEntity class."""

    credit_number: int
    amount: float
    status: str
