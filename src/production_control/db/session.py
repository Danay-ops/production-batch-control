from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeMeta, DeclarativeBase
from src.production_control.core.setings import SQLALCHEMY_DATABASE_URL

# Асинхронный URL подключения с asyncpg
SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL

# Создаем асинхронный движок
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Создаем сессию, асинхронную
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# Базовый класс — оставляем как есть, но лучше перейти на DeclarativeBase в дальнейшем
Base: DeclarativeMeta = DeclarativeBase()

# Асинхронный генератор сессий
async def get_db():
    async with SessionLocal() as db:
        yield db