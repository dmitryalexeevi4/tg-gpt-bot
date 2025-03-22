import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.utils.token import TokenValidationError

import config
from handlers import common, random, gpt_chat

TOKEN_API = config.TOKEN_TG

# Инициализируем бота и диспетчера
tg_bot = None
try:
    tg_bot = Bot(token=TOKEN_API)
except TokenValidationError:
    print('Ошибка авторизации телеграм бота, указан некорректный/пустой токен!')
dp = Dispatcher()


async def main():
    # Включаем логирование
    logging.basicConfig(level=logging.INFO)

    dp.include_router(common.router)
    dp.include_router(random.router)
    dp.include_router(gpt_chat.router)

    try:
        await dp.start_polling(tg_bot)
    except TelegramUnauthorizedError:
        print('Ошибка авторизации телеграм бота, в токене допущена ошибка!')


if __name__ == '__main__':
    asyncio.run(main())
