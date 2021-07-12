"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import UUID

from minos.common import (
    ModelType,
    Request,
    Response,
)

from .services import (
    PaymentService,
)

_Query = ModelType.build("Query", {"uuids": list[UUID]})


class PaymentController:
    """Ticket Controller class"""

    @staticmethod
    async def create_payment(request: Request) -> Response:
        """TODO

        :param request:TODO
        :return: TODO
        """
        content = await request.content()
        payment = await PaymentService().create_payment(**content)
        return Response(payment)

    @staticmethod
    async def get_payments(request: Request) -> Response:
        """TODO

        :param request: TODO
        :return: TODO
        """
        content = await request.content(model_type=_Query)
        payments = await PaymentService().get_payments(**content)
        return Response(payments)
