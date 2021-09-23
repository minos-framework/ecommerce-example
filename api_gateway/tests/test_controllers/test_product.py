import unittest

import requests
from aiohttp import web
from aiohttp.test_utils import (
    AioHTTPTestCase,
    unittest_run_loop,
)
from minos.api_gateway.common import MinosConfig
from minos.api_gateway.rest import ApiGatewayRestService

from tests.mock_servers.server import MockServer
from tests.utils import BASE_PATH


class TestProduct(AioHTTPTestCase):
    CONFIG_FILE_PATH = BASE_PATH / "config.yml"

    def setUp(self) -> None:
        self.config = MinosConfig(self.CONFIG_FILE_PATH)
        self.discovery_server = MockServer(
            host=self.config.discovery.connection.host, port=self.config.discovery.connection.port,
        )
        self.discovery_server.add_json_response(
            "/discover",
            {"ip": "localhost", "port": "5568", "name": "product", "status": True, "subscribed": True,},
            methods=("GET",),
        )

        self.order_microservice = MockServer(host="localhost", port=5568)
        self.order_microservice.add_json_response(
            "/product/5", {"testing_product_microservice": True}, methods=("GET",)
        )
        self.order_microservice.add_json_response("/product", {"product_added": 5}, methods=("POST",))
        self.order_microservice.add_json_response("/products", {"products": [3442, 223, 44242]}, methods=("GET",))

        self.discovery_server.start()
        self.order_microservice.start()
        super().setUp()

    def tearDown(self) -> None:
        self.discovery_server.shutdown_server()
        self.order_microservice.shutdown_server()
        super().tearDown()

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        app = web.Application()
        rest_interface = ApiGatewayRestService(config=self.config, app=app)

        return await rest_interface.create_application()

    @unittest_run_loop
    async def test_discovery_up_and_running(self):
        response = requests.get(
            "http://%s:%s/discover" % (self.config.discovery.connection.host, self.config.discovery.connection.port,)
        )

        self.assertEqual(200, response.status_code)

    @unittest_run_loop
    async def test_microservice_up_and_running(self):
        response = requests.get("http://localhost:5568/product/5")

        self.assertEqual(200, response.status_code)

    @unittest_run_loop
    async def test_get(self):
        resp = await self.client.request("GET", "/product/5")
        assert resp.status == 200
        text = await resp.text()
        self.assertTrue("testing_product_microservice" in text)

    @unittest_run_loop
    async def test_add(self):
        resp = await self.client.request("POST", "/product")
        assert resp.status == 200
        text = await resp.text()
        self.assertTrue("product_added" in text)

    @unittest_run_loop
    async def test_all(self):
        resp = await self.client.request("GET", "/products")
        assert resp.status == 200
        text = await resp.text()
        self.assertTrue("[3442,223,44242]" in text)


if __name__ == "__main__":
    unittest.main()
