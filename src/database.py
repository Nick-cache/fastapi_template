from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config import settings
from sqlalchemy.orm import DeclarativeBase, declared_attr
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


class BaseModel(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"


class DatabaseManager:
    engine = create_async_engine(settings.postgres.async_url)
    session_factory = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    @classmethod
    async def get_session(cls):
        async with cls.session_factory() as session:
            try:
                yield session
            except:
                await session.rollback()
                raise
            finally:
                await session.close()


session_dep = Annotated[AsyncSession, Depends(DatabaseManager.get_session)]
