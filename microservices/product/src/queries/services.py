"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import (
    AggregateDiff,
    DataTransferObject,
    Service,
)

# from minos.networks import (
#     subscribe,
# )


class ProductQueryService(Service):
    """TODO"""

    def get_products_without_stock(self) -> list[DataTransferObject]:
        """TODO

        :return: TODO
        """

    def get_most_sold_products(self, count: int) -> list[DataTransferObject]:
        """TODO

        :return: TODO
        """

    # @subscribe("ProductAdded")
    def product_added(self, diff: AggregateDiff):
        """TODO

        :param diff: TODO
        :return: TODO
        """

    # @subscribe("ProductUpdated")
    def product_updated(self, diff: AggregateDiff):
        """TODO

        :param diff: TODO
        :return: TODO
        """

    # @subscribe("ProductDeleted")
    def product_deleted(self, diff: AggregateDiff):
        """TODO

        :param diff: TODO
        :return: TODO
        """