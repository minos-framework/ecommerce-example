"""
Copyright (C) 2021 Clariteia SL
This file is part of minos framework.
Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from collections import (
    defaultdict,
)
from datetime import (
    datetime,
)
from uuid import (
    UUID,
)

from minos.common import (
    Aggregate,
    EntitySet,
    Model,
    ModelType,
)
from minos.saga import (
    Saga,
    SagaContext,
)

from ..aggregates import (
    Order,
    OrderEntry, OrderStatus,
)

PurchaseProductsQuery = ModelType.build("PurchaseProductsQuery", {"quantities": dict[str, int]})
CartQuery = ModelType.build("CartQuery", {"uuid": UUID})
PaymentQuery = ModelType.build("PaymentQuery", {"credit_number": int, "amount": float})


def _get_cart_items(context: SagaContext) -> Model:
    cart_uuid = context["cart_uuid"]
    return CartQuery(cart_uuid)


async def _process_cart_items(context: SagaContext) -> SagaContext:
    cart_products = context["products"]

    order_entries = list()
    product_uuids = list()
    order_amount = 0
    for product in cart_products:
        total_price = product.price * product.quantity
        order_amount += total_price
        order_entry = OrderEntry(total_price=total_price, unit_price=product.price, quantity=product.quantity, product=product.product_id)
        order_entries.append(order_entry)

        product_uuids.append(str(product.product_id))

    return SagaContext(order_entries=order_entries, order_amount=order_amount, product_uuids=product_uuids)

"""
async def _process_cart_items(context: SagaContext) -> SagaContext:
    cart_products = context["products"]
    order_uuid = context["order_uuid"]

    order = await Order.get_one(order_uuid)

    for product in cart_products:
        total_price = product.price * product.quantity
        order_entry = OrderEntry(total_price=total_price, unit_price=product.price, quantity=product.quantity, product=product.product_id)
        order.entries.add(order_entry)

    return SagaContext(order=order)
"""


def _purchase_products(context: SagaContext) -> Model:
    product_uuids = context['products'].product_uuids
    quantities = defaultdict(int)
    for product_uuid in product_uuids:
        quantities[str(product_uuid)] += 1

    return PurchaseProductsQuery(quantities)


def _revert_purchase_products(context: SagaContext) -> Model:
    product_uuids = context['products'].product_uuids
    quantities = defaultdict(int)
    for product_uuid in product_uuids:
        quantities[str(product_uuid)] -= 1

    return PurchaseProductsQuery(quantities)


def _payment(context: SagaContext) -> Model:
    amount = context['products'].order_amount
    card_number = context['payment_detail'].card_number
    return PaymentQuery(card_number, amount)


def _get_payment(value: Aggregate) -> UUID:
    return value.uuid


async def _create_commit_callback(context: SagaContext) -> SagaContext:
    payment_uuid = context["payment"]
    order_uuid = context["order_uuid"]
    order_entries = context['products'].order_entries
    order_amount = context['products'].order_amount

    order = await Order.get_one(order_uuid)

    for entry in order_entries:
        order.entries.add(entry)

    order.updated_at = datetime.now()
    order.payment = payment_uuid
    order.amount = order_amount
    order.status = OrderStatus.COMPLETED

    await order.save()

    return SagaContext(order=order)


CREATE_ORDER = (
    Saga("CreateOrder")
    .step()
    .invoke_participant("GetCart", _get_cart_items)
    .on_reply("products", _process_cart_items)
    .step()
    .invoke_participant("PurchaseProducts", _purchase_products)
    .with_compensation("PurchaseProducts", _revert_purchase_products)
    .step()
    .invoke_participant("CreatePayment", _payment)
    .on_reply("payment", _get_payment)
    .commit(_create_commit_callback)
)