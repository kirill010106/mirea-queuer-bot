import operator
from typing import Any

from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Format

from db.dbProcessor import clear_queue, set_lesson_to_table, get_lessons_list
from handlers.windows_handlers import delete_lesson_handler
from states.states import UserState


async def set_lesson(callback: types.CallbackQuery, widget: Any,
                     dialog_manager: DialogManager, item_id: str, **kwargs):
    lessons_list = await get_lessons_list()
    await clear_queue()
    await set_lesson_to_table(lessons_list[int(item_id)][0])
    await dialog_manager.event.answer(f"Предмет успешно изменен на {lessons_list[int(item_id)][0]}")
    await dialog_manager.switch_to(UserState.main)

lessons_kbd = Select(
    Format("{item[0]}"),
    id="lessons_kbd",
    item_id_getter=operator.itemgetter(1),
    items="lessons_list",
    on_click=set_lesson,
)

lessons_to_delete_kbd = Select(
    Format("{item[0]}"),
    id="lessons_kbd",
    item_id_getter=operator.itemgetter(1),
    items="lessons_list",
    on_click=delete_lesson_handler,
)
