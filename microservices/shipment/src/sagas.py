"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""

from minos.saga import (
    Saga,
    SagaContext,
)

from .aggregates import Shipment


def get_product(context: SagaContext):
    return context["products_query"]


async def create_shipment(products) -> Shipment:
    price = sum(product.unit_price for product in products)
    product_ids = [product.id for product in products]
    shipment = await Shipment.create(product_ids=product_ids, price=price)
    return shipment


CREATE_SHIPMENT = (
    Saga("CreateShipment")
        .step()
        .invoke_participant("GetProducts", get_product)
        .on_reply("shipment", create_shipment)
        .commit()
)
