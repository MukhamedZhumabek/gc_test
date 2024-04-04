from typing import Any
from typing import Optional

from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import JSONB

from db.base import Base
from db.base import intpk
from db.base import TimeMixin


class Product(Base, TimeMixin):
    __tablename__ = 'product'

    id: Mapped[intpk]
    name: Mapped[str]
    external_id: Mapped[str] = mapped_column(unique=True)
    description: Mapped[dict[str, Any]] = mapped_column(type_=JSONB)

    # Relations
    store_id = mapped_column(ForeignKey('store.id'))
    store = relationship('Store', back_populates='products')


class Store(Base, TimeMixin):
    __tablename__ = 'store'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]
    address: Mapped[Optional[str]]

    # Relations
    products: Mapped[list['Product']] = relationship(back_populates='store')
