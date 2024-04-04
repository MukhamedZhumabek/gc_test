from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from api.data_model.product_model import AddProduct
from api.data_model.product_model import UpdateProduct

from db.models import Product


class ProductManager:
    """
    class for making business logic
    bind web and db layers
    """
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_product_by_external_id(self, external_id: str) -> Product | None:
        """
        method return Product instance by id
        """
        try:
            stm = select(Product).where(Product.external_id == external_id)
            result = await self.db_session.execute(stm)
            return result.scalars().first()
        except NoResultFound:
            return None

    async def create_new_product(self, product: AddProduct) -> Product | None:
        """
        Add new Product instance to DB
        """
        try:
            instance = Product()
            instance.external_id = product.external_id
            instance.store_id = product.store_id
            instance.name = product.name
            instance.description = product.description

            self.db_session.add(instance)
            await self.db_session.commit()

            return instance
        except Exception:
            return None

    async def update_product(self, product: UpdateProduct) -> Product | None:
        """
        Update Product instance to DB
        (only {name, description} available to change)
        """
        try:
            stm = select(Product).where(
                and_(Product.external_id == product.external_id,
                     Product.store_id == product.store_id)
            )

            result = await self.db_session.execute(stm)

            instance = result.scalars().first()

            instance.name = product.name
            instance.description = product.description

            self.db_session.add(instance)
            await self.db_session.commit()
            return instance
        except Exception:
            return None

    async def remove_product(self, external_id: str, store_id: int):
        """
        remove Product instance from DB
        """
        try:
            stm = select(Product).where(
                and_(Product.external_id == external_id,
                     Product.store_id == store_id)
            )

            result = await self.db_session.execute(stm)
            instance = result.scalars().first()

            await self.db_session.delete(instance)
            await self.db_session.commit()

            return instance
        except Exception:
            return None