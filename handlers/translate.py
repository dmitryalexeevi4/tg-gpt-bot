from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.keyboards import translate_kb, translate_inner_kb
from utils.gpt_service import ChatGPTService

router = Router()

gpt_service = ChatGPTService()


class Translator(StatesGroup):
    language = State()
    text = State()


@router.message(Command("translate"))
async def command_translate(message: types.Message, state: FSMContext):
    await message.answer("Выберите язык для перевода:", reply_markup=translate_kb)
    await state.set_state(Translator.language)
    await state.update_data()


@router.callback_query(Translator.language)
async def language_chosen(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(language=callback.data)
    await callback.message.answer("Введите текст на русском языке:")
    await state.set_state(Translator.text)
    await callback.answer()


@router.callback_query(F.data == "change_language")
async def callback_change_language(call: types.CallbackQuery):
    await call.message.answer('Хорошо, давайте сменим язык!', reply_markup=translate_kb)


@router.callback_query(F.data == "Английский")
async def callback_eng(call: types.CallbackQuery, state: FSMContext):
    await language_chosen(call, state)


@router.callback_query(F.data == "Испанский")
async def callback_esp(call: types.CallbackQuery, state: FSMContext):
    await language_chosen(call, state)


@router.message(Translator.text)
async def text_chosen(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language")
    text = message.text

    gpt_service.add_message(
        f'Выведи текст \'{text}\' на \'{language}\' язык"')
    response = gpt_service.get_response()
    await message.answer(response, reply_markup=translate_inner_kb)

    await state.clear()
