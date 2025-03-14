from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
import asyncio

DB_USER = "postgres"
DB_PASSWORD = "apdrnlsdl1"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind = engine,
    expire_on_commit = False,
    class_ = AsyncSession
)

async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        except Exception as e:
            print(e)
            await db.rollback()
        finally:
            await db.close()

async def test_connection():
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("select * from user_info"))
        rows = result.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    asyncio.run(test_connection())