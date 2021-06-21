"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import (
    Request,
    Response,
)

from .dto import (
    FakePaymentDto,
    FakePaymentsQueryDto,
)
from .services import (
    FakePaymentService,
)


class FakePaymentController:
    """Ticket Controller class"""

    @staticmethod
    async def create_fake_payment(request: Request) -> Response:
        """TODO

        :param request:TODO
        :return: TODO
        """
        content = await request.content()
        fake_payment = await FakePaymentService().create_fake_payment(**content[0])
        return Response(fake_payment)

    @staticmethod
    async def get_fake_payments(request: Request) -> Response:
        """TODO

        :param request: TODO
        :return: TODO
        """
        content = await request.content()
        if len(content) and isinstance(content[0], FakePaymentsQueryDto):
            content = content[0].ids
        fake_payments = [
            FakePaymentDto.from_dict(fake_payment.avro_data)
            for fake_payment in await FakePaymentService().get_fake_payments(content)
        ]
        return Response(fake_payments)
