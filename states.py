from aiogram.dispatcher.filters.state import State, StatesGroup


class AddPosition(StatesGroup):
    choose_name = State()


class DeletePosition(StatesGroup):
    choose_id = State()


class AddQuestion(StatesGroup):
    choose_question_text = State()
    choose_answer_text = State()
    choose_keywords = State()
    choose_choice_mode = State()
    choose_positions = State()
