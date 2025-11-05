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

async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

