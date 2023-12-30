from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_session

DBSession = Annotated[AsyncSession, Depends(get_session)]
