"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
import unittest.async_case

from src import ProductController


class TestProductController(unittest.IsolatedAsyncioTestCase):

    async def test_create_product(self):
        controller = ProductController()
        # controller.create_product()

    async def test_get_products(self):
        controller = ProductController()
        # controller.get_products()


if __name__ == '__main__':
    unittest.main()
