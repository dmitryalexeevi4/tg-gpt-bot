from aiogram import Router, types
from aiogram.filters.command import Command

import main
from utils.gpt_service import ChatGPTService

router = Router()

gpt_service = ChatGPTService()


@router.message(Command('gpt'))
async def command_gpt(message: types.Message):
    photo = types.FSInputFile("utils/chat_gpt_pic.png")
    await main.tg_bot.send_photo(chat_id=message.chat.id, photo=photo,
                                 caption=f'Привет, {message.chat.first_name}! Введи свой запрос')


@router.message()
async def handle_message(message: types.Message):
    gpt_service.add_user_message(message.text)

    response = gpt_service.get_response()
    await message.answer(response)
