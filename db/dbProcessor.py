import asyncio
import os
import time

import aiosqlite as sq3

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


async def add_to_queue(user_id: int, user_login: str, user_name: str, checkin_time: float):
    async with sq3.connect(os.path.join(path, "queue.db")) as db:
        await db.execute("""
        INSERT OR IGNORE INTO queue (id, login, name, time) VALUES (?, ?, ?, ?)
        """, (user_id, user_login, user_name, checkin_time))
        await db.commit()


async def clear_queue():
    async with sq3.connect(os.path.join(path, "queue.db")) as db:
        await db.execute("""
        DELETE FROM queue
        """)
        await db.commit()

async def run():
    await create_table()

asyncio.run(run())
