"""
Copyright (C) 2021 Clariteia SL
This file is part of minos framework.
Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import (
    EntitySet,
)
from minos.cqrs import (
    CommandService,
)
from minos.networks import (
    Request,
    Response,
    ResponseException,
    enroute,
)
from minos.saga import (
    SagaContext,
    SagaStatus,
)

from ..aggregates import (
    PaymentDetail,
    ShipmentDetail,
)


class OrderCommandService(CommandService):
    """Ticket Service class"""

    @enroute.rest.command("/orders", "POST")
    @enroute.broker.command("CreateOrder")
    async def create_order(self, request: Request) -> Response:
        """Create a new ``Order`` instance.
        :param request: The ``Request`` containing the list of product identifiers to be included in the ``Order``.
        :return: A ``Response`` containing the ``UUID`` that identifies the ``SagaExecution``.
        """
        content = await request.content()
        cart_uuid = content["cart"]
        user_uuid = content["user"]
        payment = content["payment_detail"]
        shipment = content["shipment_detail"]

        payment_detail = PaymentDetail(**payment)
        shipment_detail = ShipmentDetail(**shipment)

        saga = await self.saga_manager.run(
            "CreateOrder",
            context=SagaContext(
                cart_uuid=cart_uuid, user_uuid=user_uuid, payment_detail=payment_detail, shipment_detail=shipment_detail
            ),
        )

        if saga.status == SagaStatus.Finished:
            return Response(dict(saga.context["order"]))
        else:
            raise ResponseException("An error occurred during order creation.")
