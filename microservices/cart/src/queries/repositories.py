from __future__ import (
    annotations,
)

from uuid import (
    UUID,
)

from minos.common import (
    FieldDiff,
    MinosConfig,
    MinosSetup,
)
from sqlalchemy import (
    and_,
    create_engine,
)
from sqlalchemy.orm import (
    sessionmaker,
)

from .models import (
    CART_ITEM_TABLE,
    CART_TABLE,
    META,
    CartDTO,
    CartItemDTO,
)


class CartQueryRepository(MinosSetup):
    """Cart inventory repository"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = create_engine("postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(**kwargs))
        self.session = sessionmaker(bind=self.engine)()

    async def _setup(self) -> None:
        META.create_all(self.engine)

    @classmethod
    def _from_config(cls, *args, config: MinosConfig, **kwargs) -> CartQueryRepository:
        return cls(*args, **(config.repository._asdict() | {"database": "cart_query_db"}) | kwargs)

    async def create_cart(self, uuid: UUID, version: int, user_id: int) -> None:
        """Insert Payment amount
        :param uuid: UUID
        :param user_id: Customer ID
        :param version: Version ID
        :return: Nothing
        """
        query = CART_TABLE.insert().values(uuid=uuid, version=version, user_id=user_id)
        self.engine.execute(query)

    async def get_cart_items(self, cart_id):
        """Insert Payment amount
        :param cart_id: UUID
        :return: Nothing
        """
        result = {}

        try:
            # Get Cart information
            cart_query = self.session.query(CART_TABLE).filter(CART_TABLE.columns.uuid == cart_id).one()
        except Exception:
            return {"error": "Invalid Cart UUID"}

        try:
            # Get Cart Item information
            cart_items_query = CART_ITEM_TABLE.select().where(CART_ITEM_TABLE.columns.cart_id == cart_id)
            cart_item_results = self.engine.execute(cart_items_query)
        except Exception:
            return {"error": "An error occurred while obtaining Cart Items."}

        try:
            # Format CartItems to DTO
            cart_items = [CartItemDTO(**row) for row in cart_item_results]

            # Format Cart DTO with Cart and CartItems attributes
            result = CartDTO(**cart_query, products=cart_items)
        except Exception:
            result = {"error": "An error occurred when formatting result."}

        return result

    async def insert_cart_item(self, cart_uuid, item_uuid, quantity, item_title, item_description, item_price):
        """Insert or Update Cart Item
        :param cart_uuid: UUID
        :param item_uuid: Customer ID
        :param quantity: Customer ID
        :param item_title: Customer ID
        :param item_description: Customer ID
        :param item_price: Customer ID
        :return: Nothing
        """
        try:
            # Insert new Cart Item Record
            query = CART_ITEM_TABLE.insert().values(
                product_id=item_uuid,
                cart_id=cart_uuid,
                quantity=quantity,
                price=item_price,
                title=item_title,
                description=item_description,
            )
            self.engine.execute(query)
        except Exception:
            return {"error": "Error inserting Cart Item."}

    async def update_cart_item(self, cart_uuid, item_uuid, quantity, item_title, item_description, item_price):
        """Insert or Update Cart Item
        :param cart_uuid: UUID
        :param item_uuid: Customer ID
        :param quantity: Customer ID
        :param item_title: Customer ID
        :param item_description: Customer ID
        :param item_price: Customer ID
        :return: Nothing
        """
        try:
            cart_item_update_query = (
                CART_ITEM_TABLE.update()
                .values(quantity=quantity, price=item_price, title=item_title, description=item_description,)
                .where(
                    and_(CART_ITEM_TABLE.columns.product_id == item_uuid, CART_ITEM_TABLE.columns.cart_id == cart_uuid,)
                )
            )
            self.engine.execute(cart_item_update_query)
        except Exception:
            return {"error": "Error updating Cart Item."}

    async def update_cart_items(self, uuid: UUID, **kwargs) -> None:
        """Update an existing row.

        :param uuid: The identifier of the row.
        :param kwargs: The parameters to be updated.
        :return: This method does not return anything.
        """
        kwargs = {k: v if not isinstance(v, FieldDiff) else v.value for k, v in kwargs.items()}

        query = CART_ITEM_TABLE.update().where(CART_ITEM_TABLE.columns.product_id == uuid).values(**kwargs)
        self.engine.execute(query)

    async def delete_cart(self, cart_uuid: UUID) -> None:
        """Delete Payment
        :param cart_uuid: UUID
        :return: Nothing
        """
        cart_delete_query = CART_TABLE.delete().where(CART_TABLE.columns.uuid == cart_uuid)
        self.engine.execute(cart_delete_query)

    async def delete_cart_item(self, cart_uuid: UUID, product_uuid: UUID) -> None:
        """Delete Payment
        :param cart_uuid: Cart UUID
        :param product_uuid: Item UUID
        :return: Nothing
        """
        delete_cart_item_query = CART_ITEM_TABLE.delete().where(
            and_(CART_ITEM_TABLE.columns.product_id == product_uuid, CART_ITEM_TABLE.columns.cart_id == cart_uuid)
        )
        self.engine.execute(delete_cart_item_query)
