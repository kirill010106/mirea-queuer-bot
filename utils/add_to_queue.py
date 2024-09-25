from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
import time as t
from db.dbProcessor import add_to_queue as write_user
from states.states import UserState


async def add_to_queue(callback: types.CallbackQuery, widget: Button, dialog_manager: DialogManager):
    user_id = callback.from_user.id
    user_name = callback.from_user.first_name
    user_login = callback.from_user.username
    time = t.time()
    await write_user(user_id, user_login, user_name, time)
    await callback.answer("Вы успешно записались в очередь на ответ!")
    await dialog_manager.switch_to(UserState.main)
