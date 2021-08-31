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
    enroute,
)
from minos.saga import (
    SagaContext,
)

from ..aggregates import (
    Order,
    OrderStatus,
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
        payment = content["payment"]
        shipment = content["shipment"]

        payment_detail = PaymentDetail(**payment)
        shipment_detail = ShipmentDetail(**shipment)

        order = await Order.create(
            entries=EntitySet(),
            payment_detail=payment_detail,
            shipment_detail=shipment_detail,
            status=OrderStatus.CREATED,
            user=user_uuid,
        )

        uuid = await self.saga_manager.run(
            "CreateOrder",
            context=SagaContext(cart_uuid=cart_uuid, order_uuid=order.uuid, payment_detail=payment_detail),
        )
        return Response(uuid)
