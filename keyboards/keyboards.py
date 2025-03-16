from aiogram import types

start_button = types.KeyboardButton(text='/start')
random_button = types.KeyboardButton(text='/random')
gpt_button = types.KeyboardButton(text='/gpt')
talk_button = types.KeyboardButton(text='/talk')
quiz_button = types.KeyboardButton(text='/quiz')
# translate_button = types.KeyboardButton(text='/translate')
# recommend_button = types.KeyboardButton(text='/recommend')
stop_button = types.KeyboardButton(text='/stop')

main_keyboard_list = [
    [start_button, random_button],
    [gpt_button, talk_button],
    [quiz_button, stop_button]
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
    [types.InlineKeyboardButton(text="Сменить тему", callback_data='change_theme')],
    [types.InlineKeyboardButton(text="Закончить", callback_data='callback_stop')]
]

main_kb = types.ReplyKeyboardMarkup(keyboard=main_keyboard_list, resize_keyboard=True)
stop_kb = types.InlineKeyboardMarkup(
    inline_keyboard=[[types.InlineKeyboardButton(text="Закончить", callback_data='callback_stop')]])
random_kb = types.InlineKeyboardMarkup(inline_keyboard=inline_random_kb_list)
talk_kb = types.InlineKeyboardMarkup(inline_keyboard=inline_talk_kb_list)
quiz_kb = types.InlineKeyboardMarkup(inline_keyboard=inline_quiz_kb_list)
quiz_inner_kb = types.InlineKeyboardMarkup(inline_keyboard=inline_quiz_inner_kb_list)
