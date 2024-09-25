import logging

from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode, ShowMode

from dialogs.dialogs import main_dialog
from states.states import UserState

router = Router()
router.include_router(main_dialog)


@router.message(CommandStart())
async def start(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=UserState.main, mode=StartMode.RESET_STACK)


async def on_unknown_intent(event, dialog_manager: DialogManager):
    logging.error("Restarting dialog: %s", event.exception)
    await dialog_manager.start(UserState.reload, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND)
