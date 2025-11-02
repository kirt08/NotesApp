from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from utils import DB_URL

engine = create_async_engine(DB_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)


Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

