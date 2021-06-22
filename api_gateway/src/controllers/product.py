"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from aiohttp import web
from minos.api_gateway.common import MinosConfig
from minos.api_gateway.rest import MicroserviceCallCoordinator


class ProductController:
    async def add(self, request: web.Request, config: MinosConfig, **kwargs):
        coordinator = MicroserviceCallCoordinator(config, request)
        response = await coordinator.orchestrate()
        return response

    async def get(self, request: web.Request, config: MinosConfig, **kwargs):
        coordinator = MicroserviceCallCoordinator(config, request)
        response = await coordinator.orchestrate()
        return response

    async def all_products(self, request: web.Request, config: MinosConfig,
                           **kwargs):
        coordinator = MicroserviceCallCoordinator(config, request)
        response = await coordinator.orchestrate()
        return response
