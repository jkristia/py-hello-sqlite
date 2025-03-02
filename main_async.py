
# database.py
import asyncio
import os
import subprocess
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Define the Table1 model
class Table1(Base):
    __tablename__ = 'Table1'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    description = Column(String, nullable=False)

# Define the Table2 model
class Table2(Base):
    __tablename__ = 'Table2'
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)


# Define the async Database class
class Database:
    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url, echo=True)
        self.AsyncSession = async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def run_migrations(self):
        # Run Alembic migrations
        # alembic_path = os.path.join(os.path.dirname(__file__), 'alembic')
        alembic_path = os.path.join(os.path.dirname(__file__))
        subprocess.call(['alembic', '-c', f'{alembic_path}/alembic.ini', 'upgrade', 'head'])

# Usage example
async def main():
    db = Database("sqlite+aiosqlite:///db_async.db")
    await db.create_tables()
    await db.run_migrations()
    print("Tables created and migrations applied successfully!")

if __name__ == "__main__":
    asyncio.run(main())
