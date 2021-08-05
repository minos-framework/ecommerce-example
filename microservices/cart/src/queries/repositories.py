"""
Copyright (C) 2021 Clariteia SL
This file is part of minos framework.
Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from __future__ import (
    annotations,
)

from typing import (
    NoReturn,
)
from uuid import (
    UUID,
)

from minos.common import (
    MinosConfig,
    PostgreSqlMinosDatabase,
)


class CartRepository(PostgreSqlMinosDatabase):
    """Cart inventory repository"""

    async def _setup(self) -> NoReturn:
        await self.submit_query(_CREATE_CART_TABLE)
        await self.submit_query(_CREATE_CART_ITEM_TABLE)

    @classmethod
    def _from_config(cls, *args, config: MinosConfig, **kwargs) -> CartRepository:
        return cls(*args, **(config.repository._asdict() | {"database": "cart_query_db"}) | kwargs)

    async def create_cart(self, uuid: UUID, user_id: int) -> NoReturn:
        """ Insert Payment amount
        :param uuid: UUID
        :param user_id: User ID
        :return: Nothing
        """
        await self.submit_query(_INSERT_CART_QUERY, {"uuid": uuid, "user_id": user_id})

    async def get_cart_items(self, cart_id):
        """ Insert Payment amount
        :param cart_id: UUID
        :return: Nothing
        """
        items = [v async for v in self.submit_query_and_iter(_SELECT_CART_ITEMS_QUERY, {"cart_id": cart_id})]
        return items

    async def insert_or_update_cart_item(
        self, cart_uuid, item_uuid, quantity, item_title, item_description, item_price
    ):
        """ Insert or Update Cart Item
        :param cart_uuid: UUID
        :param item_uuid: User ID
        :param quantity: User ID
        :param item_title: User ID
        :param item_description: User ID
        :param item_price: User ID
        :return: Nothing
        """

        await self.submit_query(
            _INSERT_CART_ITEM_QUERY,
            {
                "cart_id": cart_uuid,
                "product_id": item_uuid,
                "quantity": quantity,
                "title": item_title,
                "description": item_description,
                "price": item_price,
            },
        )

    async def delete_cart(self, cart_uuid: UUID) -> NoReturn:
        """ Delete Payment
        :param cart_uuid: UUID
        :return: Nothing
        """
        await self.submit_query(_DELETE_CART_QUERY, {"cart_uuid": cart_uuid})

    async def delete_cart_item(self, cart_uuid: UUID, product_uuid: UUID) -> NoReturn:
        """ Delete Payment
        :param cart_uuid: Cart UUID
        :param product_uuid: Item UUID
        :return: Nothing
        """
        await self.submit_query(_DELETE_CART_ITEM_QUERY, {"cart_id": cart_uuid, "product_id": product_uuid})


_CREATE_CART_TABLE = """
CREATE TABLE IF NOT EXISTS cart (
    uuid UUID NOT NULL PRIMARY KEY,
    user_id INT NOT NULL
);
""".strip()

_CREATE_CART_ITEM_TABLE = """
CREATE TABLE IF NOT EXISTS items (
    product_id UUID NOT NULL,
    cart_id UUID NOT NULL,
    quantity INT NOT NULL,
    title VARCHAR(255),
    description VARCHAR(255),
    price FLOAT,
    primary key(cart_id, product_id),
    CONSTRAINT fk_cart
      FOREIGN KEY(cart_id)
	    REFERENCES cart(uuid)
	    ON DELETE CASCADE
);
""".strip()

_INSERT_CART_QUERY = """
INSERT INTO cart (uuid, user_id)
VALUES (%(uuid)s,  %(user_id)s)
ON CONFLICT (uuid)
DO
   UPDATE SET user_id = %(user_id)s
;
""".strip()

_INSERT_CART_ITEM_QUERY = """
INSERT INTO items (cart_id, product_id, quantity, title, description, price)
VALUES (%(cart_id)s, %(product_id)s,  %(quantity)s,  %(title)s,  %(description)s,  %(price)s)
ON CONFLICT (product_id, cart_id)
DO
   UPDATE SET quantity = %(quantity)s
;
""".strip()

_SELECT_CART_ITEMS_QUERY = """
SELECT cart_id, product_id, quantity, title, description, price FROM items WHERE cart_id=%(cart_id)s;
""".strip()

_DELETE_CART_QUERY = """
DELETE FROM cart
WHERE uuid = %(cart_uuid)s;
""".strip()

_DELETE_CART_ITEM_QUERY = """
DELETE FROM cart
WHERE product_id = %(product_id)s and cart_id = %(cart_id)s;
""".strip()
