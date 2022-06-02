from collections import (
    defaultdict,
)
from uuid import (
    UUID,
)

from minos.common import (
    Inject,
    ModelType,
)
from minos.saga import (
    Saga,
    SagaContext,
    SagaRequest,
    SagaResponse,
    RemoteSagaStep,
    LocalSagaStep,
)

from ..aggregates import (
    OrderAggregate,
)


@Saga()
class CreateOrderSaga:
    """TODO"""

    PurchaseProductsQuery = ModelType.build("PurchaseProductsQuery", {"quantities": dict[str, int]})
    TicketQuery = ModelType.build("TicketQuery", {"cart_uuid": UUID})
    PaymentQuery = ModelType.build("PaymentQuery", {"credit_number": int, "amount": float})

    @Inject()
    def __init__(self, aggregate: OrderAggregate):
        self.aggregate = aggregate

    @RemoteSagaStep(order=1)
    def _create_ticket(self, context: SagaContext) -> SagaRequest:
        cart_uuid = context["cart_uuid"]
        return SagaRequest("CreateTicket", self.TicketQuery(cart_uuid))

    @_create_ticket.on_success()
    async def _process_ticket_entries(self, context: SagaContext, response: SagaResponse) -> SagaContext:
        ticket = await response.content()
        product_uuids = list()
        for entry in ticket.entries.data.values():
            product_uuids.append(str(entry.product))
        context["ticket"] = dict(uuid=ticket.uuid, product_uuids=product_uuids, total_amount=ticket.total_price)
        return context

    @RemoteSagaStep(order=2)
    def _purchase_products(self, context: SagaContext) -> SagaRequest:
        product_uuids = context["ticket"]["product_uuids"]
        quantities = defaultdict(int)
        for product_uuid in product_uuids:
            quantities[str(product_uuid)] += 1

        return SagaRequest("PurchaseProducts", self.PurchaseProductsQuery(quantities))

    @_purchase_products.on_error()
    def _raise(self, context: SagaContext, response: SagaResponse) -> SagaContext:
        raise ValueError("Errored response must abort the execution!")

    @_purchase_products.on_failure()
    def _revert_purchase_products(self, context: SagaContext) -> SagaRequest:
        product_uuids = context["ticket"]["product_uuids"]
        quantities = defaultdict(int)
        for product_uuid in product_uuids:
            quantities[str(product_uuid)] -= 1

        return SagaRequest("PurchaseProducts", self.PurchaseProductsQuery(quantities))

    @RemoteSagaStep(order=3)
    def _payment(self, context: SagaContext) -> SagaRequest:
        amount = context["ticket"]["total_amount"]
        card_number = context["payment_detail"].card_number
        return SagaRequest("CreatePayment", self.PaymentQuery(card_number, amount))

    @_payment.on_success()
    async def _get_payment(self, context: SagaContext, response: SagaResponse) -> SagaContext:
        value = await response.content()
        context["payment"] = value.uuid
        return context

    @LocalSagaStep(order=4)
    async def _create_commit_callback(self, context: SagaContext) -> SagaContext:
        order = await self.aggregate.create_order_instance(
            ticket=context["ticket"]["uuid"],
            payment=context["payment"],
            payment_detail=context["payment_detail"],
            shipment_detail=context["shipment_detail"],
            total_amount=context["ticket"]["total_amount"],
            customer=context["customer_uuid"],
        )
        return SagaContext(order=order)
