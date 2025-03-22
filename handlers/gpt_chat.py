from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from openai import BadRequestError

import main
from keyboards.keyboards import talk_kb, stop_kb, quiz_kb, quiz_inner_kb, translate_inner_kb, translate_kb, main_kb, \
    recommend_inner_kb, recommend_kb
from utils.gpt_service import ChatGPTService

router = Router()

gpt_service = ChatGPTService()


class StateForm(StatesGroup):
    name = State()


class Translator(StatesGroup):
    language = State()
    text = State()


class Recommends(StatesGroup):
    category = State()
    genre = State()


'''
Команда /gpt
'''


@router.message(Command('gpt'))
async def command_gpt(message: types.Message, state: FSMContext):
    gpt_service.clear_message_history()
    photo = types.FSInputFile("utils/chat_gpt_pic.png")
    await main.tg_bot.send_photo(chat_id=message.chat.id, photo=photo,
                                 caption=f'Привет, {message.chat.first_name}! Введи свой запрос')
    await state.set_state(StateForm.name)
    await state.update_data(name='gpt')


'''
Команда /talk
'''


@router.message(Command('talk'))
async def command_talk(message: types.Message, state: FSMContext):
    gpt_service.clear_message_history()
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


'''
Команда /quiz
'''


@router.message(Command('quiz'))
async def command_quiz(message: types.Message, state: FSMContext):
    gpt_service.clear_message_history()
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


'''
Команда /translate
'''


@router.message(Command("translate"))
async def command_translate(message: types.Message, state: FSMContext):
    gpt_service.clear_message_history()
    await message.answer("Выберите язык для перевода:", reply_markup=translate_kb)
    await state.set_state(StateForm.name)
    await state.update_data(name='translate')
    await state.set_state(Translator.language)
    await state.update_data()


@router.callback_query(Translator.language)
async def language_chosen(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(language=callback.data)
    await callback.message.answer("Введите текст для перевода:")
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

    if message.content_type == 'text':
        gpt_service.add_message(
            f'Выведи текст \'{text}\' на \'{language}\' язык"')
        response = gpt_service.get_response()
        await message.answer(response, reply_markup=translate_inner_kb)
    else:
        await message.answer(
            "Отсутствует реализация обработки файлов/голосовых сообщений, используйте текст! Возвращаемся в меню бота..",
            reply_markup=main_kb)
        await state.clear()
        gpt_service.clear_message_history()


'''
Команда /recommend
'''


@router.message(Command("recommend"))
async def command_recommend(message: types.Message, state: FSMContext):
    gpt_service.clear_message_history()
    await message.answer("Выберите категорию рекомендаций:", reply_markup=recommend_kb)
    await state.set_state(StateForm.name)
    await state.update_data(name='recommend')
    await state.set_state(Recommends.category)
    await state.update_data()


@router.callback_query(Recommends.category)
async def category_chosen(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data)
    category = await state.get_value('category')
    await callback.message.answer(f"Выбрана категория '{category}', введите жанр:")
    await state.set_state(Recommends.genre)
    await callback.answer()


@router.callback_query(F.data == "show_more")
async def callback_show_more(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    category = user_data.get("category")
    genre = user_data.get("genre")

    gpt_service.add_message(
        f'Подбери мне еще один результат в категории\'{category}\' в жанре \'{genre}\'.')
    response = gpt_service.get_response()
    await call.message.answer(response, reply_markup=recommend_inner_kb)


@router.callback_query(F.data == "Фильмы")
async def callback_films(call: types.CallbackQuery, state: FSMContext):
    await category_chosen(call, state)


@router.callback_query(F.data == "Книги")
async def callback_books(call: types.CallbackQuery, state: FSMContext):
    await category_chosen(call, state)


@router.callback_query(F.data == "Музыка")
async def callback_music(call: types.CallbackQuery, state: FSMContext):
    await category_chosen(call, state)


@router.message(Recommends.genre)
async def genre_chosen(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    category = user_data.get("category")
    genre = message.text
    await state.update_data(genre=genre)

    if message.content_type == 'text':
        gpt_service.add_message(
            f'Подбери мне \'{category}\' в жанре \'{genre}\'. Выведи самый удачный результат')
        response = gpt_service.get_response()
        await message.answer(response, reply_markup=recommend_inner_kb)
    else:
        await message.answer(
            "Отсутствует реализация обработки файлов/голосовых сообщений, используйте текст! Возвращаемся в меню бота..",
            reply_markup=main_kb)
        await state.clear()
        gpt_service.clear_message_history()


'''
Обработчик сообщений
'''


@router.message()
async def handle_message(message: types.Message, state: FSMContext):
    data = await state.get_data()

    if len(data) == 0:
        await message.answer("Выберите кнопку в меню/на сообщении!")
    else:
        gpt_service.add_message(message.text)
        response = None
        try:
            response = gpt_service.get_response()
        except BadRequestError:
            await message.answer(
                "Отсутствует реализация обработки файлов/голосовых сообщений, используйте текст! Возвращаемся в меню бота..",
                reply_markup=main_kb)
            await state.clear()
            gpt_service.clear_message_history()

        if message.text == 'gpt' or data['name'] == 'gpt':
            await message.answer(response)
        elif message.text == 'talk' or data['name'] == 'talk':
            await message.answer(response, reply_markup=stop_kb)
        elif message.text == 'quiz' or data['name'] == 'quiz':
            await message.answer(response, reply_markup=quiz_inner_kb)
        elif message.text == 'translate' or data['name'] == 'translate':
            await message.answer(response, reply_markup=translate_inner_kb)
        elif message.text == 'recommend' or data['name'] == 'recommend':
            await message.answer(response, reply_markup=recommend_inner_kb)
