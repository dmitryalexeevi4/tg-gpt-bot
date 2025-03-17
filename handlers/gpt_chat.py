from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import main
from keyboards.keyboards import talk_kb, stop_kb, quiz_kb, quiz_inner_kb
from utils.gpt_service import ChatGPTService

router = Router()

gpt_service = ChatGPTService()


class StateForm(StatesGroup):
    name = State()


@router.message(Command('gpt'))
async def command_gpt(message: types.Message, state: FSMContext):
    photo = types.FSInputFile("utils/chat_gpt_pic.png")
    await main.tg_bot.send_photo(chat_id=message.chat.id, photo=photo,
                                 caption=f'Привет, {message.chat.first_name}! Введи свой запрос')
    await state.set_state(StateForm.name)
    await state.update_data(name='gpt')


@router.message(Command('talk'))
async def command_talk(message: types.Message, state: FSMContext):
    photo = types.FSInputFile("utils/talk_pic.png")
    await main.tg_bot.send_photo(chat_id=message.chat.id, photo=photo, caption="Выберите известную личность:",
                                 reply_markup=talk_kb)
    await state.set_state(StateForm.name)
    await state.update_data(name='talk')


@router.callback_query(F.data == "putin_type")
async def callback_putin_type(call: types.CallbackQuery):
    gpt_service.add_message(
        "Отвечай мне с уверенным, взвешенным и стратегически выверенным тоном. Представься именем Владимир")
    response = gpt_service.get_response()
    await call.message.answer(response, reply_markup=stop_kb)


@router.callback_query(F.data == "bezrukov_type")
async def callback_putin_type(call: types.CallbackQuery):
    gpt_service.add_message(
        "Отвечай мне с душой, по-русски, с размахом! Представься именем Сергей")
    response = gpt_service.get_response()
    await call.message.answer(response, reply_markup=stop_kb)


@router.callback_query(F.data == "semenovich_type")
async def callback_putin_type(call: types.CallbackQuery):
    gpt_service.add_message(
        "Отвечай мне с лёгкостью, теплотой и капелькой искры! Представься именем Анна")
    response = gpt_service.get_response()
    await call.message.answer(response, reply_markup=stop_kb)


@router.message(Command('quiz'))
async def command_quiz(message: types.Message, state: FSMContext):
    photo = types.FSInputFile("utils/quiz_pic.png")
    await main.tg_bot.send_photo(chat_id=message.chat.id, photo=photo, caption="Выберите тему для квиза:",
                                 reply_markup=quiz_kb)
    await state.set_state(StateForm.name)
    await state.update_data(name='quiz')


async def start_quiz_theme(call: types.CallbackQuery, theme: str):
    gpt_service.add_message(
        f'Ты задаешь мне вопрос на тему \'{theme}\' и предлагаешь мне 4 варианта ответов. '
        'Ты ведешь счет правильных и неправильных ответов"')
    response = gpt_service.get_response()
    await call.message.answer(response, reply_markup=quiz_inner_kb)


@router.callback_query(F.data == "modern_music_theme")
async def callback_modern_music(call: types.CallbackQuery):
    theme = "Современная музыка"
    await start_quiz_theme(call, theme)


@router.callback_query(F.data == "modern_cinema_theme")
async def callback_modern_cinema(call: types.CallbackQuery):
    theme = "Современное кино"
    await start_quiz_theme(call, theme)


@router.callback_query(F.data == "gamedev_industry_theme")
async def callback_gamedev_industry(call: types.CallbackQuery):
    theme = "Игровая индустрия"
    await start_quiz_theme(call, theme)


@router.callback_query(F.data == "one_more")
async def callback_change_theme(call: types.CallbackQuery):
    gpt_service.add_message('Еще один вопрос')
    response = gpt_service.get_response()
    await call.message.answer(response, reply_markup=quiz_inner_kb)


@router.callback_query(F.data == "change_theme")
async def callback_change_theme(call: types.CallbackQuery):
    await call.message.answer('Хорошо, давайте сменим тему!', reply_markup=quiz_kb)


@router.message()
async def handle_message(message: types.Message, state: FSMContext):
    gpt_service.add_message(message.text)
    response = gpt_service.get_response()

    data = await state.get_data()

    if message.text == 'gpt' or data['name'] == 'gpt':
        await message.answer(response)
    elif message.text == 'talk' or data['name'] == 'talk':
        await message.answer(response, reply_markup=stop_kb)
    elif message.text == 'quiz' or data['name'] == 'quiz':
        await message.answer(response, reply_markup=quiz_inner_kb)
