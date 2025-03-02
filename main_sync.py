#directly copied from copilot
# database.py
import os
import subprocess
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Initialize the base class for declarative models
Base = declarative_base()

# Define the Table1 model
class Table1(Base):
    __tablename__ = 'Table1'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    tag = Column(String)

# Define the Table1 model
class Table2(Base):
    __tablename__ = 'Table2'
    id = Column(Integer, primary_key=True)
    description = Column(String)


# Define the Database class
class Database:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)

    def run_migrations(self):
        # Run Alembic migrations
        # alembic_path = os.path.join(os.path.dirname(__file__), 'alembic')
        alembic_path = os.path.join(os.path.dirname(__file__))
        subprocess.call(['alembic', '-c', f'{alembic_path}/alembic.ini', 'upgrade', 'head'])


# Usage example
if __name__ == "__main__":
    db = Database("sqlite:///db_sync.sqlite")
    db.create_tables()
    db.run_migrations()
    print("Tables created successfully!")
