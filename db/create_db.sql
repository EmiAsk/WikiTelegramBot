--
-- Файл сгенерирован с помощью SQLiteStudio v3.2.1 в Вт июл 20 20:41:04 2021
--
-- Использованная кодировка текста: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: pos_to_question
CREATE TABLE pos_to_question (position_id INTEGER REFERENCES positions (id), question_id INTEGER REFERENCES questions (id));

-- Таблица: positions
CREATE TABLE positions (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, name STRING UNIQUE NOT NULL);

-- Таблица: questions
CREATE TABLE questions (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, question STRING NOT NULL, answer TEXT NOT NULL, keywords STRING);

-- Таблица: users
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, tg_id INTEGER NOT NULL UNIQUE, position_id INTEGER REFERENCES positions (id));

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
