from aiogram import Router, types, F
from aiogram.filters.command import Command

import main
from keyboards.keyboards import random_kb
from utils.gpt_service import ChatGPTService

router = Router()

gpt_service = ChatGPTService()


# /random
@router.message(Command('random'))
async def command_random(message: types.Message):
    photo = types.FSInputFile("utils/random_pic.png")

    gpt_service.add_message("Рандомный факт")
    response = gpt_service.get_response()

    await main.tg_bot.send_photo(chat_id=message.chat.id, photo=photo, caption=response, reply_markup=random_kb)


@router.callback_query(F.data == "more_random")
async def callback_more_random_func(call: types.CallbackQuery):
    photo = types.FSInputFile("utils/random_pic.png")

    gpt_service.add_message("Рандомный факт")
    response = gpt_service.get_response()

    await call.bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=response, reply_markup=random_kb)
