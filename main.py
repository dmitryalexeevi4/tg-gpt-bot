import asyncio
import logging

from aiogram import Bot, Dispatcher

import config
from handlers import common, gpt_chat, talk, quiz, random

TOKEN_API = config.TOKEN_TG

# Инициализируем бота и диспетчера
tg_bot = Bot(token=TOKEN_API)
dp = Dispatcher()


async def main():
    # Включаем логирование
    logging.basicConfig(level=logging.INFO)

    dp.include_router(common.router)
    dp.include_router(random.router)
    dp.include_router(gpt_chat.router)
    dp.include_router(talk.router)
    dp.include_router(quiz.router)

    await dp.start_polling(tg_bot)


if __name__ == '__main__':
    asyncio.run(main())
