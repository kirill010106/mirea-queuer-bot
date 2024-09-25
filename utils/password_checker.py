from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from states.states import UserState
from config_data.config import load_config

config = load_config()


async def is_password_correct(message: types.Message, widget: MessageInput, dialog_manager: DialogManager):
    if str(message.text) == config.tg_bot.admin_password:
        await dialog_manager.switch_to(UserState.choose_lesson)
        await message.delete()
    else:
        await message.answer("Неверный пароль, попробуйте еще раз или вернитесь в меню")
