from fastapi import Depends
from fastapi import APIRouter
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_db_session

from api.data_model.product_model import AddProduct
from api.data_model.product_model import UpdateProduct
from api.data_model.product_model import ProductResponse

from manager.product_manager import ProductManager as Manager

product_router = APIRouter(tags=['product'])


@product_router.get("/{external_id}", response_model=ProductResponse)
async def get(external_id: str, db_session: AsyncSession = Depends(get_db_session)) -> ProductResponse:
    """
    Get Product by external id
    """
    product = await Manager(db_session).get_product_by_external_id(external_id=external_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return product


@product_router.post("/", response_model=ProductResponse)
async def post(product_model: AddProduct, db_session: AsyncSession = Depends(get_db_session)) -> ProductResponse:
    """
    Create new product
    """
    product = await Manager(db_session).create_new_product(product=product_model)
    if not product:
        raise HTTPException(
            status_code=400,
            detail="Uncorrected payload data"
        )
    return product


@product_router.put("/", response_model=ProductResponse)
async def put(product_model: UpdateProduct, db_session: AsyncSession = Depends(get_db_session)) -> ProductResponse:
    """
    Update product by external_id and store_id
    """
    product = await Manager(db_session).update_product(product=product_model)

    if not product:
        raise HTTPException(
            status_code=400,
            detail="Uncorrected payload data")

    return product


@product_router.delete("/{external_id}/{store_id}",
                       response_model=ProductResponse)
async def delete(external_id: str,
                 store_id: int, db_session: AsyncSession = Depends(get_db_session)) -> ProductResponse:
    """
    Remove Product by external_id and store_id
    """
    product = await Manager(db_session).remove_product(
        external_id=external_id,
        store_id=store_id
    )
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return product
