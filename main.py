import asyncio
import logging

from aiogram import Bot, Dispatcher

import config
from handlers import common, translate, random, gpt_chat

TOKEN_API = config.TOKEN_TG

# Инициализируем бота и диспетчера
tg_bot = Bot(token=TOKEN_API)
dp = Dispatcher()


async def main():
    # Включаем логирование
    logging.basicConfig(level=logging.INFO)

    dp.include_router(common.router)
    dp.include_router(random.router)
    dp.include_router(translate.router)
    dp.include_router(gpt_chat.router)

    await dp.start_polling(tg_bot)


if __name__ == '__main__':
    asyncio.run(main())
