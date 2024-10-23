import asyncio
import os
import time

import aiosqlite as sq3
from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from states.states import UserState

path = os.path.dirname(os.path.realpath(__file__))


async def create_table():
    async with sq3.connect(os.path.join(path, "queue.db")) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS queue(
            id INTEGER PRIMARY KEY NOT NULL,
            login INTEGER,
            name STRING,
            time INTEGER)
            """)
        await db.commit()


async def create_lesson_table():
    async with sq3.connect(os.path.join(path, "lesson.db")) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS lesson(
            lesson STRING PRIMARY KEY NOT NULL)
            """)
        await db.commit()


async def create_lessons_table():
    async with sq3.connect(os.path.join(path, "lessons.db")) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS lessons(
            lesson STRING NOT NULL,
            id INTEGER UNIQUE,
            PRIMARY KEY("id" AUTOINCREMENT))
            """)
        await db.commit()


async def get_lessons_list() -> list:
    await create_lessons_table()
    async with sq3.connect(os.path.join(path, "lessons.db")) as db:
        cur = await db.execute("""
            SELECT * FROM lessons
            """)
        res = list(await cur.fetchall())
        await db.commit()
        return res


async def add_lesson_to_db(lesson: str):
    await create_lesson_table()
    async with sq3.connect(os.path.join(path, "lessons.db")) as db:
        await db.execute("""
        INSERT OR IGNORE INTO lessons (lesson) VALUES (?)
        """, (lesson,))
        await db.commit()


async def delete_lesson_from_db(id: int):
    await create_lessons_table()
    async with sq3.connect(os.path.join(path, "lessons.db")) as db:
        await db.execute("""
        DELETE FROM lessons WHERE id = ?
        """, (id,))
        await db.commit()


async def set_lesson_to_table(lesson: str):
    async with sq3.connect(os.path.join(path, "lesson.db")) as db:
        await db.execute("DELETE FROM lesson")
        await db.commit()
        await db.execute("""
            INSERT OR IGNORE INTO lesson (lesson) VALUES (?)
            """, (lesson,))
        await db.commit()


async def get_lesson_from_table():
    async with sq3.connect(os.path.join(path, "lesson.db")) as db:
        cur = await db.execute("SELECT * FROM lesson")
        try:
            res = list(await cur.fetchone())[0]
        except TypeError:
            return None
        return res


async def add_to_queue(user_id: int, user_login: str, user_name: str, checkin_time: float):
    async with sq3.connect(os.path.join(path, "queue.db")) as db:
        await db.execute("""
        INSERT OR IGNORE INTO queue (id, login, name, time) VALUES (?, ?, ?, ?)
        """, (user_id, user_login, user_name, checkin_time))
        await db.commit()


async def remove_from_queue(user_id: int):
    async with sq3.connect(os.path.join(path, "queue.db")) as db:
        await db.execute("DELETE FROM queue WHERE id=?", (user_id,))
        await db.commit()


async def remove_from_queue_output(callback: types.CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await remove_from_queue(callback.from_user.id)
    await callback.answer("Вы вышли из очереди.")
    await dialog_manager.switch_to(UserState.main)


async def _get_queue():
    async with sq3.connect(os.path.join(path, "queue.db")) as db:
        cur = await db.execute("SELECT * FROM queue ORDER BY time")
        queue_list = await cur.fetchall()
    return queue_list


async def pass_queue():
    count = 1
    format_queue = ""
    lst = await _get_queue()
    if lst:
        for i in lst:
            if i[1]:
                format_queue += str(count) + ". " + "@" + i[1] + " : " + i[2] + "\n"
            else:
                format_queue += str(count) + ". " + i[2] + "\n"
            # await callback.message.answer(str(count) + ". " + "@" + i[1] + " : " + i[2] + " UNIX: " + str(i[3]))
            count += 1
        return format_queue
    else:
        return "Очередь в данный момент пуста."


async def clear_queue():
    async with sq3.connect(os.path.join(path, "queue.db")) as db:
        await db.execute("""
        DELETE FROM queue
        """)
        await db.commit()

# async def run():
#     ...
#
# asyncio.run(run())
