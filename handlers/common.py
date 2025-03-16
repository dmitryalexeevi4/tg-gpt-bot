from aiogram import Router, types, F
from aiogram.filters.command import Command

from keyboards.keyboards import main_kb
from utils.gpt_service import ChatGPTService

router = Router()

gpt_service = ChatGPTService()


@router.message(Command('start'))
async def command_start(message: types.Message):
    await message.answer(f'Привет, {message.chat.first_name}! я Chat-GPT Bot, проект Java Rush University!',
                         reply_markup=main_kb)


@router.message(Command('stop'))
async def command_start(message: types.Message):
    await message.answer('Хорошо, возвращаемся в меню бота!', reply_markup=main_kb)


@router.callback_query(F.data == "callback_stop")
async def callback_stop_func(call: types.CallbackQuery):
    await call.message.answer('Хорошо, возвращаемся в меню бота!', reply_markup=main_kb)
