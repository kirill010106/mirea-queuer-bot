import operator
from typing import Any

from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Format

from db.lessons import lessons
from db.queues import lessonsQueue
from states.states import UserState

from db.dbProcessor import clear_queue, set_lesson_to_table


async def set_lesson(callback: types.CallbackQuery, widget: Any,
                     dialog_manager: DialogManager, item_id: str, **kwargs):
    await clear_queue()
    await set_lesson_to_table(lessons[int(item_id)][0])
    await dialog_manager.event.answer(f"Предмет успешно изменен на {lessons[int(item_id)][0]}")
    # lessonsQueue.get(lessons[int(item_id)])[0] = {}
    await dialog_manager.switch_to(UserState.main)

lessons_kbd = Select(
    Format("{item[0]}"),
    id="lessons_kbd",
    item_id_getter=operator.itemgetter(1),
    items="lessons",
    on_click=set_lesson,
)
