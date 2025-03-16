from aiogram import Router, types, F
from aiogram.filters.command import Command

import main
from keyboards.keyboards import quiz_kb, quiz_inner_kb
from utils.gpt_service import ChatGPTService

router = Router()

gpt_service = ChatGPTService()


async def start_quiz_theme(call: types.CallbackQuery, theme_description: str):
    gpt_service.add_user_message(theme_description)
    try:
        response = gpt_service.get_response()
        await call.message.answer(response, reply_markup=quiz_inner_kb)
    except Exception as e:
        await call.message.answer("Произошла ошибка. Попробуйте снова.", reply_markup=quiz_inner_kb)


@router.message(Command('quiz'))
async def command_quiz(message: types.Message):
    photo = types.FSInputFile("utils/quiz_pic.png")
    await main.tg_bot.send_photo(chat_id=message.chat.id, photo=photo, caption="Выберите тему для квиза:",
                                 reply_markup=quiz_kb)


@router.callback_query(F.data == "modern_music_theme")
async def callback_modern_music(call: types.CallbackQuery):
    theme_description = "Давай сыграем в квиз на тему современной музыки, ты задаешь вопрос и предлагаешь мне 4 варианта ответов, следующий вопрос задаешь сразу после того как получишь мой ответ"
    await start_quiz_theme(call, theme_description)


@router.callback_query(F.data == "modern_cinema_theme")
async def callback_modern_cinema(call: types.CallbackQuery):
    theme_description = "Давай сыграем в квиз на тему современного кино, ты задаешь вопрос и предлагаешь мне 4 варианта ответов, следующий вопрос задаешь сразу после того как получишь мой ответ"
    await start_quiz_theme(call, theme_description)


@router.callback_query(F.data == "gamedev_industry_theme")
async def callback_gamedev_industry(call: types.CallbackQuery):
    theme_description = "Давай сыграем в квиз на тему игровой индустрии, ты задаешь вопрос и предлагаешь мне 4 варианта ответов, следующий вопрос задаешь сразу после того как получишь мой ответ"
    await start_quiz_theme(call, theme_description)


@router.callback_query(F.data == "change_theme")
async def callback_change_theme(call: types.CallbackQuery):
    await call.message.answer('Хорошо, давайте сменим тему!', reply_markup=quiz_kb)


@router.message()
async def handle_message(message: types.Message):
    gpt_service.add_user_message(message.text)
    try:
        response = gpt_service.get_response()
        await message.answer(response, reply_markup=quiz_inner_kb)
    except Exception as e:
        await message.answer("Произошла ошибка при обработке вашего сообщения. Попробуйте позже.")
