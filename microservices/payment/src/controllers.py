"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import Request, Response

from .services import PaymentService


class PaymentController:
    """Ticket Controller class"""

    @staticmethod
    async def create_payment(request: Request) -> Response:
        """TODO

        :param request:TODO
        :return: TODO
        """
        content = await request.content()
        payment = await PaymentService().create_payment(**content[0])
        return Response(payment)

    @staticmethod
    async def get_payments(request: Request) -> Response:
        """TODO

        :param request: TODO
        :return: TODO
        """
        content = await request.content()
        if len(content) and hasattr(content[0], "ids"):
            content = content[0].ids
        else:
            content = list(map(int, content))
        payments = await PaymentService().get_payments(content)
        return Response(payments)
