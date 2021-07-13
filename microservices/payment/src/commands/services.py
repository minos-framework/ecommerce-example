"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import (
    UUID,
)

from minos.common import (
    ModelType,
    Request,
    Response,
    Service,
)

from ..aggregates import (
    Payment,
)


class PaymentCommandService(Service):
    """Ticket Service class"""

    @staticmethod
    async def create_payment(request: Request) -> Response:
        """Create a payment

        :param request: TODO
        :return: TODO
        """
        content = await request.content()
        credit_number = content["credit_number"]
        amount = content["amount"]
        status = "created"

        payment = await Payment.create(credit_number, amount, status)

        return Response(payment)

    @staticmethod
    async def get_payments(request: Request) -> Response:
        """TODO

        :param request: TODO
        :return: TODO
        """
        _Query = ModelType.build("Query", {"uuids": list[UUID]})
        content = await request.content(model_type=_Query)
        uuids = content["uuids"]

        values = {v.uuid: v async for v in Payment.get(uuids=uuids)}
        payments = [values[uuid] for uuid in uuids]

        return Response(payments)
