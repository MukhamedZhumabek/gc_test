from fastapi import FastAPI
from fastapi import Depends

from api.router.auth import authorize
from api.router.product_router import product_router
from api.router.store_router import store_router

gc_test_app = FastAPI(title='Global Coffee Test App')

gc_test_app.include_router(
    store_router,
    prefix='/api/v1/store',
    dependencies=[Depends(authorize)]
)

gc_test_app.include_router(
    product_router,
    prefix='/api/v1/product',
    dependencies=[Depends(authorize)]
)
