from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List, Tuple


positions_callback = CallbackData('admin', 'id_', 'name')
choice_mode_callback = CallbackData('admin', 'mode')


def get_position_choice_kb(positions: List[Tuple[int, str]]):
    keyboard = InlineKeyboardMarkup(row_width=1)

    for position in positions:
        id_, name = position
        pos_callback = positions_callback.new(id_=id_, name=name)
        button = InlineKeyboardButton(text=f'{id_} - {name}',
                                      callback_data=pos_callback)
        keyboard.add(button)

    confirm_button = InlineKeyboardButton(text='Подтвердить',
                                          callback_data='admin:confirm')
    keyboard.add(confirm_button)

    return keyboard


def get_positions_choice_mode_kb():
    keyboard = InlineKeyboardMarkup(row_width=1)

    for text, mode in (('Все', 'all'), ('Кроме', 'except'), ('Некоторые', 'some'), ('Ничего', 'nothing')):
        button = InlineKeyboardButton(text=text, callback_data=choice_mode_callback.new(mode=mode))
        keyboard.add(button)

    return keyboard







