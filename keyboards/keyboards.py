from aiogram import types

random_button = types.KeyboardButton(text='/random')
gpt_button = types.KeyboardButton(text='/gpt')
talk_button = types.KeyboardButton(text='/talk')
quiz_button = types.KeyboardButton(text='/quiz')
translate_button = types.KeyboardButton(text='/translate')
recommend_button = types.KeyboardButton(text='/recommend')

main_keyboard_list = [
    [random_button, gpt_button],
    [talk_button, quiz_button],
    [translate_button, recommend_button]
]

inline_random_kb_list = [
    [types.InlineKeyboardButton(text="Хочу ещё факт", callback_data='more_random')],
    [types.InlineKeyboardButton(text="Закончить", callback_data='callback_stop')]
]

inline_talk_kb_list = [
    [types.InlineKeyboardButton(text="Владимир Путин", callback_data='putin_type')],
    [types.InlineKeyboardButton(text="Сергей Безруков", callback_data='bezrukov_type')],
    [types.InlineKeyboardButton(text="Анна Семенович", callback_data='semenovich_type')]
]

inline_quiz_kb_list = [
    [types.InlineKeyboardButton(text="Современная музыка", callback_data='modern_music_theme')],
    [types.InlineKeyboardButton(text="Современное кино", callback_data='modern_cinema_theme')],
    [types.InlineKeyboardButton(text="Игровая индустрия", callback_data='gamedev_industry_theme')]
]

inline_quiz_inner_kb_list = [
    [types.InlineKeyboardButton(text="Еще вопрос", callback_data='one_more')],
    [types.InlineKeyboardButton(text="Сменить тему", callback_data='change_theme')],
    [types.InlineKeyboardButton(text="Закончить", callback_data='callback_stop')]
]

inline_translate_kb_list = [
    [types.InlineKeyboardButton(text="Английский", callback_data='Английский')],
    [types.InlineKeyboardButton(text="Испанский", callback_data='Испанский')]
]

inline_translate_inner_kb_list = [
    [types.InlineKeyboardButton(text="Сменить язык", callback_data='change_language')],
    [types.InlineKeyboardButton(text="Закончить", callback_data='callback_stop')]
]

inline_recommend_kb_list = [
    [types.InlineKeyboardButton(text="Фильмы", callback_data='Фильмы')],
    [types.InlineKeyboardButton(text="Книги", callback_data='Книги')],
    [types.InlineKeyboardButton(text="Музыка", callback_data='Музыка')]
]

inline_recommend_inner_kb_list = [
    [types.InlineKeyboardButton(text="Не нравится", callback_data='show_more')],
    [types.InlineKeyboardButton(text="Закончить", callback_data='callback_stop')]
]

main_kb = types.ReplyKeyboardMarkup(keyboard=main_keyboard_list, resize_keyboard=True)
stop_kb = types.InlineKeyboardMarkup(
    inline_keyboard=[[types.InlineKeyboardButton(text="Закончить", callback_data='callback_stop')]])
random_kb = types.InlineKeyboardMarkup(inline_keyboard=inline_random_kb_list)
talk_kb = types.InlineKeyboardMarkup(inline_keyboard=inline_talk_kb_list)
quiz_kb = types.InlineKeyboardMarkup(inline_keyboard=inline_quiz_kb_list)
quiz_inner_kb = types.InlineKeyboardMarkup(inline_keyboard=inline_quiz_inner_kb_list)
translate_kb = types.InlineKeyboardMarkup(inline_keyboard=inline_translate_kb_list)
translate_inner_kb = types.InlineKeyboardMarkup(inline_keyboard=inline_translate_inner_kb_list)
recommend_kb = types.InlineKeyboardMarkup(inline_keyboard=inline_recommend_kb_list)
recommend_inner_kb = types.InlineKeyboardMarkup(inline_keyboard=inline_recommend_inner_kb_list)
