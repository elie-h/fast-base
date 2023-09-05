from typing import AsyncGenerator
from databases import Database
from app.db import db


async def get_db() -> AsyncGenerator[Database, None]:
    yield db
