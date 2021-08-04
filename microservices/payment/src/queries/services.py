"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from typing import (
    NoReturn,
)
from uuid import (
    UUID,
)

from dependency_injector.wiring import (
    Provide,
)
from minos.common import (
    UUID_REGEX,
    AggregateDiff,
    ModelType,
)
from minos.cqrs import (
    QueryService,
)
from minos.networks import (
    Request,
    Response,
    ResponseException,
    enroute,
)

from .repositories import (
    PaymentAmountRepository,
)


class PaymentQueryService(QueryService):
    """Payment Query Service class"""

    repository: PaymentAmountRepository = Provide["payment_amount_repository"]

    @staticmethod
    @enroute.broker.query("GetPayments")
    @enroute.rest.query("/payments", "GET")
    async def get_payments(request: Request) -> Response:
        """Get payments.

        :param request: The ``Request`` instance that contains the payment identifiers.
        :return: A ``Response`` instance containing the requested payments.
        """
        try:
            content = await request.content(model_type=ModelType.build("Query", {"uuids": list[UUID]}))
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        try:
            from ..aggregates import (
                Payment,
            )

            iterable = Payment.get(uuids=content["uuids"])
            values = {v.uuid: v async for v in iterable}
            payments = [values[uuid] for uuid in content["uuids"]]
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting payments: {exc!r}")

        return Response(payments)

    @staticmethod
    @enroute.broker.query("GetPayment")
    @enroute.rest.query(f"/payments/{{uuid:{UUID_REGEX.pattern}}}", "GET")
    async def get_payment(request: Request) -> Response:
        """Get payment.

        :param request: The ``Request`` instance that contains the payment identifier.
        :return: A ``Response`` instance containing the requested payment.
        """
        from minos.common import (
            ModelType,
        )

        try:
            content = await request.content(model_type=ModelType.build("Query", {"uuid": UUID}))
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        try:
            from ..aggregates import (
                Payment,
            )

            payment = await Payment.get_one(content["uuid"])
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting the payment: {exc!r}")

        return Response(payment)

    @enroute.broker.event("PaymentCreated")
    @enroute.broker.event("PaymentUpdated")
    async def payment_created_or_updated(self, request: Request) -> NoReturn:
        """Handle the payment create events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        uuid = diff.uuid
        amount = diff.fields_diff["amount"]

        await self.repository.insert_payment_amount(uuid, amount)

    @enroute.broker.event("PaymentDeleted")
    async def payment_deleted(self, request: Request) -> NoReturn:
        """Handle the payment delete events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()

        await self.repository.delete(diff.uuid)
