import asyncio
import logging

from aiogram import Dispatcher, Bot, F
from aiogram.types import BotCommand
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from handlers import user
from middlewares.db import DbSessionMiddleware
from config import Config
from db.repo import proceed_schemas
from middlewares.user import UserMiddleware


async def start_b():

    config = Config()

    logging.basicConfig(level=logging.DEBUG)

    bot = Bot(token=config.bot.token, parse_mode="HTML")

    engine = create_async_engine(config.postgres_dsn, future=True)
    db_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    await proceed_schemas(engine)

    dp = Dispatcher()

    dp.message.filter(F.chat.type == "private")

    dp.update.outer_middleware(DbSessionMiddleware(db_pool))
    dp.update.outer_middleware(UserMiddleware())

    dp.include_router(user.router)

    dp["db_pool"] = db_pool

    await bot.set_my_commands(commands=[BotCommand(command="start", description="Головне меню")])
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=["message", "callback_query", "inline_query", "chat_member", "chat_join_request"])


if __name__ == "__main__":
    asyncio.run(start_b())