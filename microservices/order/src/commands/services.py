"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.cqrs import CommandService
from minos.networks import (
    Request,
    Response,
    enroute,
)
from minos.saga import SagaContext


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
        product_uuids = content["product_uuids"]
        uuid = await self.saga_manager.run(
            "CreateOrder", context=SagaContext(product_uuids=product_uuids), pause_on_disk=True, return_execution=False
        )
        return Response(uuid)
