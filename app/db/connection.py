from sqlalchemy import create_engine, MetaData
from databases import Database
from app.core.config import config


# Databases query wrapper
db = Database(config.DATABASE_URL)

# Traditional SQLAlchemy engine used for Alembic and other synchronous operations that need DB access.
metadata = MetaData()
engine = create_engine(config.DATABASE_URL.replace("+asyncpg", ""), pool_pre_ping=True, echo=True)
