from loader import dp
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from states import AddQuestion
from text_of_answers import text_responses
from db_helper import db_get_all_questions, db_get_all_positions, db_add_question, db_add_rel_pos_to_question,\
    db_delete_question, db_get_question_by_id
from typing import List, Tuple, Dict, NamedTuple
from keyboards.inline.admin_menu import get_position_choice_kb, positions_callback, choice_mode_callback, \
    get_positions_choice_mode_kb


class ChoiceMode:
    all_ = 'all'
    some = 'some'
    except_ = 'except'
    nothing = 'nothing'


def check_id(args: list):
    if not args or len(args) != 1 or not args[0].isdigit():
        return False
    return True


@dp.message_handler(commands=['list_q'], is_admin=True)
async def get_list_of_questions(message: Message):
    questions: List[Tuple] = db_get_all_questions()
    await message.answer(text_responses.questions_list(questions))


@dp.message_handler(commands=['add_q'], is_admin=True)
async def cmd_add_question(message: Message):
    await message.answer(text_responses.add_question_text)
    await AddQuestion.first()


@dp.message_handler(commands=['del_q'], is_admin=True)
async def cmd_delete_question(message: Message):
    args = message.get_args().split()

    if not check_id(args):
        await message.answer(text_responses.wrong_chosen_q_id)
        return

    is_added: bool = db_delete_question(id_=args[0])
    if not is_added:
        await message.answer(text_responses.question_does_not_exists)
        return

    await message.answer(text_responses.question_is_deleted)


@dp.message_handler(commands=['get_q'], is_admin=True)
async def cmd_get_question(message: Message):
    args = message.get_args().split()

    if not check_id(args):
        await message.answer(text_responses.wrong_chosen_q_id)
        return

    question = db_get_question_by_id(id_=args[0])
    if not question:
        await message.answer(text_responses.question_does_not_exists)
        return

    await message.answer(text_responses.one_question(question[0]))


@dp.message_handler(is_admin=True, state=AddQuestion.choose_question_text)
async def choose_question_text(message: Message, state: FSMContext):
    question_text: str = message.text
    await state.update_data(question_text=question_text)
    await message.answer(text_responses.question_text_is_added)
    await message.answer(text_responses.add_answer_text)
    await AddQuestion.choose_answer_text.set()


@dp.message_handler(is_admin=True, state=AddQuestion.choose_answer_text)
async def choose_answer_text(message: Message, state: FSMContext):
    answer_text: str = message.text
    await state.update_data(answer_text=answer_text)
    await message.answer(text_responses.answer_text_is_added)
    await message.answer(text_responses.add_keywords)
    await AddQuestion.next()


@dp.message_handler(is_admin=True, state=AddQuestion.choose_keywords)
async def choose_keywords(message: Message, state: FSMContext):
    keywords_list: List[str] = message.text.split()
    await state.update_data(keywords=keywords_list)

    keyboard: InlineKeyboardMarkup = get_positions_choice_mode_kb()
    await message.answer(text_responses.keywords_are_added)
    await message.answer(text_responses.choose_choice_mode, reply_markup=keyboard)
    await AddQuestion.choose_choice_mode.set()


@dp.callback_query_handler(choice_mode_callback.filter(mode=[ChoiceMode.all_, ChoiceMode.nothing]),
                           state=AddQuestion.choose_choice_mode)
async def choose_all_or_none_mode(call: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()

    inserted_id = db_add_question(answer_text=data['answer_text'],
                                  question_text=data['question_text'],
                                  keywords=data['keywords'])
    if callback_data['mode'] == ChoiceMode.all_:
        db_add_rel_pos_to_question(question_id=inserted_id)

    await call.message.answer(text_responses.question_is_added)
    await state.finish()
    await call.answer()


@dp.callback_query_handler(choice_mode_callback.filter(), state=AddQuestion.choose_choice_mode)
async def choose_some_choice_mode(call: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    data['mode'] = callback_data['mode']
    await state.update_data(data)

    positions = db_get_all_positions()
    keyboard: InlineKeyboardMarkup = get_position_choice_kb(positions)
    await call.message.answer(text_responses.chosen_positions_list, reply_markup=keyboard)

    await AddQuestion.choose_positions.set()
    await call.answer()


@dp.callback_query_handler(positions_callback.filter(), is_admin=True,
                           state=AddQuestion.choose_positions)
async def choose_positions(call: CallbackQuery, callback_data: dict, state: FSMContext):
    pos_id = callback_data.get('id_')
    pos_name = callback_data.get('name')

    if pos_id is not None:
        pos_id = int(pos_id)

    data = await state.get_data()

    chosen_positions = data.get('chosen_positions', {})
    if pos_id in chosen_positions:
        del chosen_positions[pos_id]
    else:
        chosen_positions[pos_id] = pos_name

    await state.update_data({'chosen_positions': chosen_positions})
    await update_positions_text(call, chosen_positions)
    await call.answer()


@dp.callback_query_handler(text='admin:confirm', is_admin=True,
                           state=AddQuestion.choose_positions)
async def confirm_positions_choice(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    inserted_id = db_add_question(answer_text=data['answer_text'],
                                  question_text=data['question_text'],
                                  keywords=data['keywords'])
    positions = data['chosen_positions'].keys()

    if data['mode'] == ChoiceMode.except_:
        all_positions = set(map(lambda pos: pos[0], db_get_all_positions()))
        positions = (all_positions - set(positions))

    db_add_rel_pos_to_question(question_id=inserted_id, positions=positions)

    await call.message.edit_text(text_responses.question_is_added)
    await state.finish()
    await call.answer()


async def update_positions_text(call: CallbackQuery, positions: Dict[int, str]):
    text = text_responses.positions_list(list(positions.items()))
    await call.message.edit_text(text=text_responses.chosen_positions_list + text,
                                 reply_markup=call.message.reply_markup)
