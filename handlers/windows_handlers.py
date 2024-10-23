from typing import Any

from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Select

from db.dbProcessor import add_lesson_to_db, delete_lesson_from_db
from states.states import UserState


async def add_lesson_handler(message: types.Message, widget: MessageInput, dialog_manager: DialogManager):
    await add_lesson_to_db(message.text)
    await dialog_manager.event.answer("Пара успешно добавлена!")
    await dialog_manager.start(UserState.main)


async def delete_lesson_handler(callback: types.CallbackQuery, widget: Select,
                                dialog_manager: DialogManager, item_id: str, **kwargs):
    await delete_lesson_from_db(int(item_id))
    await dialog_manager.event.message.answer("Пара успешно удалена!")
    await dialog_manager.start(UserState.main)
