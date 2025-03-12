from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import session_getter


SessionDep = Annotated[AsyncSession, Depends(session_getter)]