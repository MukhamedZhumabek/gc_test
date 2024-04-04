import pytest

from starlette.testclient import TestClient

from main import gc_test_app

from db.base import Base
from db.base import async_engine
from db.base import async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_db():
    """
    Clean database before start tests
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='session')
async def get_async_session():
    """Provide async AsyncSession for connect to DB"""
    yield async_session


@pytest.fixture(scope='function')
async def client():
    with TestClient(gc_test_app) as client:
        yield client
