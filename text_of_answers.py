from collections import namedtuple
from typing import Tuple, List


def format_list_of_positions(positions: List[Tuple[int, str]]) -> str:
    return '\n\n'.join(f'ID: {id_}\nДолжность: {name}' for id_, name in positions)


def format_list_of_questions(questions: List[Tuple]) -> str:
    return '\n\n'.join(f'ID: {id_}\nТекст вопроса: {question}'
                       for id_, question, _, _ in questions)


def format_one_question(question: tuple) -> str:
    id_, q_text, a_text, keywords = question
    return f'''ID: {id_}\nВопрос: {q_text}\nОтвет: {a_text}\nКлючевые слова: {keywords}'''


RESPONSES_TYPES = ('welcome', 'help', 'wrong_chosen_pos_name',
                   'name_already_exists', 'add_position',
                   'delete_position', 'position_is_added', 'action_was_cancelled',
                   'positions_list', 'wrong_chosen_pos_id', 'position_does_not_exists',
                   'position_is_deleted', 'questions_list', 'add_question_text',
                   'add_answer_text', 'add_keywords', 'question_text_is_added',
                   'answer_text_is_added', 'keywords_are_added', 'chosen_positions_list',
                   'choose_choice_mode', 'question_is_added', 'wrong_chosen_q_id', 'question_is_deleted',
                   'question_does_not_exists', 'one_question')

PlainAnswers = namedtuple('PlainAnswers', RESPONSES_TYPES)

text_responses = PlainAnswers(welcome='Приветствую!',
                              help='',
                              wrong_chosen_pos_name='Это не похоже на название должности. Повторите ввод',
                              wrong_chosen_pos_id='Это не похоже на ID должности. Повторите ввод',
                              position_does_not_exists='Должности с данным ID не существует. Повторите ввод.',
                              delete_position='Введите ID должности (из списка должностей),'
                                              'которую хотите удалить'
                                              'или отправьте /cancel, чтобы вернуться назад',

                              add_position='Введите название должности, которую'
                                           'хотите добавить или отправьте /cancel,',
                              name_already_exists='Данное имя должности уже занято. Повторите ввод',
                              position_is_added='Должность успешно добавлена',
                              position_is_deleted='Должность успешно удалена',
                              action_was_cancelled='Действие было отменено!',
                              add_question_text='Введите текст вопроса, который хотите добавить.',
                              question_text_is_added='Текст вопроса успешно добавлен.',
                              add_answer_text='Теперь введите ответ на этот вопрос.',
                              answer_text_is_added='Текст ответа на вопрос успешно добавлен.',
                              add_keywords='Теперь введите ключевые слова,'
                                           'по которым будет выполнятся поиск вопросов.\n'
                                           'Пример:\n"работа\nдосуг\nотдых"\n\nИЛИ\n\n"работа досуг отдых"',
                              keywords_are_added='Ключевые слова успешно добавлены',
                              chosen_positions_list='Список выбранных должностей, которым доступен вопрос:\n\n',
                              choose_choice_mode='Выберите режим выбора позиций',
                              question_is_added='Вопрос успешно добавлен!',
                              wrong_chosen_q_id='Это не похоже на ID вопроса. Повторите ввод.',
                              question_is_deleted='Вопрос успешно удалён',
                              question_does_not_exists='Вопроса с данным ID не существует.',
                              positions_list=format_list_of_positions,
                              questions_list=format_list_of_questions,
                              one_question=format_one_question)
