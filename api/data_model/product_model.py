from pydantic import BaseModel


class AddProduct(BaseModel):
    external_id: str
    name: str
    description: dict
    store_id: int


class UpdateProduct(BaseModel):
    external_id: str
    name: str
    description: dict
    store_id: int


class ProductResponse(AddProduct):
    id: int

