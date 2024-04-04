from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.data_model.store_model import StoreResponse, AddStore
from db.base import get_db_session
from manager.store_manager import StoreManager as Manager

store_router = APIRouter(tags=['store'])


@store_router.get("/{store_id}", response_model=StoreResponse)
async def get(store_id: int, db_session: AsyncSession = Depends(get_db_session)) -> StoreResponse:
    """
    Get Store by id
    """
    store = await Manager(db_session).get_store_by_id(store_id=store_id)

    if not store:
        raise HTTPException(
            status_code=404,
            detail="Store not found"
        )
    return store


@store_router.post("/", response_model=StoreResponse)
async def post(store_model: AddStore, db_session: AsyncSession = Depends(get_db_session)) -> StoreResponse:
    """
    Create new Store
    """
    store = await Manager(db_session).create_new_store(store=store_model)
    if not store:
        raise HTTPException(
            status_code=400,
            detail="Uncorrected payload data"
        )
    return store