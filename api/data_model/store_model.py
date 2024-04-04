from typing import Optional, List

from pydantic import BaseModel

from api.data_model.product_model import ProductResponse


class AddStore(BaseModel):
    name: str
    description: Optional[str]
    address: Optional[str]


class StoreResponse(AddStore):
    products: Optional[List[ProductResponse]]

