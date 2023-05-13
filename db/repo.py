from math import ceil
from typing import List

from sqlalchemy.ext.asyncio import AsyncEngine

from config import Config
from db.base.base import Base
from db.base.repo import BaseRepo

from datetime import datetime, timedelta

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User


async def proceed_schemas(async_engine: AsyncEngine) -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class Repo(BaseRepo):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def add_user(self, id: int, fullname: str, username: str) -> None:
        user = User(id=id, fullname=fullname, username=username)
        await self.commit(user)

    async def get_user(self, id: int):
        stmt = select(User).where(User.id == id)
        return await self._scalar(stmt)
