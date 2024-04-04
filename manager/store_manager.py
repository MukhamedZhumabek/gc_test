from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.data_model.store_model import AddStore
from db.models import Store


class StoreManager:
    """
    class for making business logic
    bind web and db layers
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_store_by_id(self, store_id: int) -> Store | None:
        """
        Method return Store instance by id
        """
        try:
            stm = (
                select(Store).where(Store.id == store_id)
                .options(selectinload(Store.products))
            )
            result = await self.db_session.execute(stm)
            store = result.scalars().first()
            return store
        except NoResultFound:
            return None

    async def create_new_store(self, store: AddStore) -> Store | None:
        """
        Add new Store instance to DB
        """
        try:
            instance = Store()
            instance.name = store.name
            instance.description = store.description
            instance.address = store.address
            instance.products = []

            self.db_session.add(instance)
            await self.db_session.commit()

            return instance
        except Exception:
            return None
