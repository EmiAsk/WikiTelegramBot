from sqlite3 import connect, Cursor
import os
from config import DATABASE_PATH
from sqlite3 import IntegrityError
from typing import Tuple, List, Iterator, Iterable

FILENAME = 'db_wiki.db'


def connect_to_db(func):
    def inner(*args, **kwargs):
        with connect(os.path.join(DATABASE_PATH, FILENAME)) as connection:
            cursor = connection.cursor()
            result = func(*args, **kwargs, cursor=cursor)
            connection.commit()
            return result

    return inner


@connect_to_db
def db_add_position(name, cursor: Cursor) -> bool:
    request = '''INSERT INTO positions(name) VALUES (?)'''
    try:
        cursor.execute(request, (name,))
        return True
    except IntegrityError:
        return False


@connect_to_db
def db_get_position_by_id(id_, cursor: Cursor):
    request = '''SELECT * FROM positions WHERE id = ?'''
    cursor.execute(request, (id_, ))
    position: List[Tuple[int, str]] = cursor.fetchall()
    return position


@connect_to_db
def db_delete_position(id_, cursor: Cursor) -> bool:
    request = '''DELETE FROM positions WHERE id = ?'''
    if not db_get_position_by_id(id_):
        return False

    cursor.execute(request, (id_,))
    return True


@connect_to_db
def db_get_all_positions(cursor: Cursor):
    request = '''SELECT * FROM positions'''
    cursor.execute(request)
    return cursor.fetchall()


@connect_to_db
def db_get_all_questions(cursor: Cursor) -> List[Tuple]:
    request = '''SELECT * FROM questions'''
    cursor.execute(request)
    return cursor.fetchall()


def db_add_question(question_text: str, answer_text: str, keywords: list) -> int:
    request = '''INSERT INTO questions(question, answer, keywords) VALUES (?, ?, ?)'''

    with connect(os.path.join(DATABASE_PATH, FILENAME)) as connection:
        cursor = connection.cursor()
        cursor.execute(request, (question_text, answer_text, ', '.join(keywords)))
        connection.commit()

    return cursor.lastrowid


@connect_to_db
def db_add_rel_pos_to_question(question_id: int, cursor: Cursor, positions: Iterable[int] = None):
    request = f'''INSERT INTO pos_to_question VALUES (?, {question_id})'''
    if positions is not None:
        positions = map(lambda pos: (pos,), positions)
    else:
        positions = map(lambda pos: (pos[0],), db_get_all_positions())

    cursor.executemany(request, positions)


@connect_to_db
def db_delete_relations(cursor: Cursor, question_id: int = None, position_id: int = None):
    request = '''DELETE FROM pos_to_question WHERE'''

    cond = ''
    if (question_id and position_id) or not (question_id or position_id):
        raise ValueError
    elif question_id is None:
        cond = f' position_id = {position_id}'
    elif position_id is None:
        cond = f' question_id = {question_id}'

    cursor.execute(request + cond)


@connect_to_db
def db_delete_question(id_: int, cursor: Cursor):
    request = '''DELETE FROM questions WHERE id = ?'''

    if not db_get_question_by_id(id_):
        return False

    db_delete_relations(question_id=id_)
    cursor.execute(request, (id_,))
    return True


@connect_to_db
def db_get_question_by_id(id_: int, cursor: Cursor):
    request = '''SELECT * FROM questions WHERE id = ?'''

    cursor.execute(request, (id_,))
    return cursor.fetchall()


def init_db():
    with open('db/create_db.sql') as file:
        sql_script = file.read()

    with connect(os.path.join(DATABASE_PATH, FILENAME)) as connection:
        cursor = connection.cursor()
        cursor.executescript(sql_script)
        connection.commit()