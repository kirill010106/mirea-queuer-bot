from aiogram_dialog import DialogManager
from db.lessons import lessons


async def current_lesson_getter(dialog_manager: DialogManager, **kwargs):
    # TODO ADD CURRENT LESSON TO DB
    if dialog_manager.dialog_data.get("current_lesson"):
        return {
            "current_lesson": dialog_manager.dialog_data["current_lesson"]
        }
    else:
        return {
            "current_lesson": "[Нужно выставить пару...]"
        }


async def lessons_getter(**kwargs):
    return {
        "lessons": lessons,
    }
