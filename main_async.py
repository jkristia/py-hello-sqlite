import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence

Base = declarative_base()

class Table1(Base):
    __tablename__ = 'table_1'
    id = Column(Integer, Sequence('id'), primary_key=True)
    name = Column(String(50))
    value = Column(Integer)
    tag = Column(String)

class Table2(Base):
    __tablename__ = 'table_2'
    id = Column(Integer, Sequence('id'), primary_key=True)
    name = Column(String(50))
    value = Column(Integer)


class Database:
    def __init__(self, database_url: str):
        self._engine = create_async_engine(database_url, echo=True)
        self._session = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def init_db(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def add_value(self, name: str, value: int):
        async with self._session() as session:
            async with session.begin():
                new_item = Table1(name=name, value=value)
                session.add(new_item)
                await session.commit()

async def main():
    db = Database('sqlite+aiosqlite:///foo_async.sqlite')
    await db.init_db()
    await db.add_value('Example', 123)

asyncio.run(main())
