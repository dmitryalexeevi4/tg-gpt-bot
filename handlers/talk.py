from aiogram import Router, types, F
from aiogram.filters.command import Command

import main
from keyboards.keyboards import talk_kb, stop_kb
from utils.gpt_service import ChatGPTService

router = Router()

gpt_service = ChatGPTService()


async def handle_gpt_response(message: types.Message, tone: str = None):
    if tone:
        gpt_service.add_message(tone)
    else:
        gpt_service.add_message(message.text)

    try:
        response = gpt_service.get_response()
        await message.answer(response, reply_markup=stop_kb)
    except Exception as e:
        await message.answer("Произошла ошибка при обработке запроса. Попробуйте снова.")


@router.message(Command('talk'))
async def command_talk(message: types.Message):
    photo = types.FSInputFile("utils/talk_pic.png")
    await main.tg_bot.send_photo(chat_id=message.chat.id, photo=photo, caption="Выберите известную личность:",
                                 reply_markup=talk_kb)


@router.callback_query(F.data == "putin_type")
async def callback_putin_type(call: types.CallbackQuery):
    await handle_gpt_response(call.message,
                              "Отвечай мне с уверенным, взвешенным и стратегически выверенным тоном. Представься именем Владимир")


@router.callback_query(F.data == "bezrukov_type")
async def callback_bezrukov_type(call: types.CallbackQuery):
    await handle_gpt_response(call.message, "Отвечай мне с душой, по-русски, с размахом! Представься именем Сергей")


@router.callback_query(F.data == "semenovich_type")
async def callback_semenovich_type(call: types.CallbackQuery):
    await handle_gpt_response(call.message,
                              "Отвечай мне с лёгкостью, теплотой и капелькой искры! Представься именем Анна")


@router.message()
async def handle_message(message: types.Message):
    await handle_gpt_response(message)
