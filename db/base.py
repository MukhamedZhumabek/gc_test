import datetime

from typing import Annotated
from typing import Generator

from sqlalchemy import text
from sqlalchemy import NullPool

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase

from settings import sqlalchemy_url

async_engine = create_async_engine(sqlalchemy_url, future=True, poolclass=NullPool)

async_session = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    pass


class TimeMixin:
    """
    Mixin to add timestamp fields to models
    """
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=text("TIMEZONE('utc', now())")
    )


async def get_db_session() -> Generator:
    """
    Dependency, return async session for connect ot DB
    """
    try:
        session = async_session()
        yield session
    finally:
        await session.close()
