from aiogram import types
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button

from states.states import UserState


async def reload_window(callback: types.CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(UserState.main, show_mode=ShowMode.EDIT)
