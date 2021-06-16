from aiohttp import web
from minos.api_gateway.common import MinosConfig
from minos.api_gateway.rest import MicroserviceCallCoordinator


class Order:
    async def add(self, request: web.Request, config: MinosConfig, **kwargs):
        coordinator = MicroserviceCallCoordinator(
            config, request, request.url.host, request.url.port
        )
        response = await coordinator.orchestrate()
        return response

    async def get(self, request: web.Request, config: MinosConfig, **kwargs):
        coordinator = MicroserviceCallCoordinator(
            config, request, request.url.host, request.url.port
        )
        response = await coordinator.orchestrate()
        return response

    async def history(self, request: web.Request, config: MinosConfig, **kwargs):
        coordinator = MicroserviceCallCoordinator(
            config, request, request.url.host, request.url.port
        )
        response = await coordinator.orchestrate()
        return response