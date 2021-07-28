from aiogram import dispatcher
import handlers
from aiogram import executor
from aiogram.dispatcher.filters import Text
from loader import dp
from aiogram.types import Message
from filters.filters import IsAdmin
from states import AddPosition, DeletePosition
from aiogram.dispatcher import FSMContext
from text_of_answers import text_responses
from db_helper import db_add_position, db_get_all_positions, db_delete_position
from typing import Tuple, List

# def errors(f):
#     async def inner(*args, **kwargs):
#         try:
#             return await f()
#         except Exception as er:
#             print(er)
#
#     return inner


@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    await message.answer(text_responses.welcome)


@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: Message, state: FSMContext):
    await state.reset_state(with_data=False)
    await message.answer(text_responses.action_was_cancelled)


@dp.message_handler(commands=['add_pos'], is_admin=True)
@dp.message_handler(Text(equals='Добавить должность', ignore_case=True), is_admin=True)
async def cmd_add_position(message: Message):
    await message.answer(text_responses.add_position)
    await AddPosition.first()


@dp.message_handler(state=AddPosition.choose_name, is_admin=True)
async def add_position(message: Message, state: FSMContext):
    pos_name = message.text

    if not pos_name.isalnum() or pos_name.isdigit():
        await message.answer(text_responses.wrong_chosen_pos_name)
        return

    name_is_added = db_add_position(name=pos_name)
    if not name_is_added:
        await message.answer(text_responses.name_already_exists)
        return

    await message.answer(text_responses.position_is_added)
    await state.finish()


@dp.message_handler(commands=['list'], is_admin=True)
@dp.message_handler(Text(equals='Список должностей', ignore_case=True), is_admin=True)
async def get_list_of_positions(message: Message):
    positions: List[Tuple[int, str]] = db_get_all_positions()
    await message.answer(text_responses.positions_list(positions))


@dp.message_handler(commands=['delete_pos'], is_admin=True)
@dp.message_handler(Text(equals='Удалить должность', ignore_case=True), is_admin=True)
async def cmd_delete_position(message: Message):
    await message.answer(text_responses.delete_position)
    await DeletePosition.first()


@dp.message_handler(state=DeletePosition.choose_id)
async def delete_position(message: Message, state: FSMContext):
    chosen_id = message.text
    if not chosen_id.isdigit():
        await message.answer(text_responses.wrong_chosen_pos_id)
        return

    pos_deleted = db_delete_position(chosen_id)
    if not pos_deleted:
        await message.answer(text_responses.position_does_not_exists)
        return

    await message.answer(text_responses.position_is_deleted)
    await state.reset_state(with_data=False)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)
