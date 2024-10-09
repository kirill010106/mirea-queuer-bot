from aiogram_dialog import DialogManager
from db.lessons import lessons
from db.dbProcessor import pass_queue


async def current_lesson_and_queue_getter(dialog_manager: DialogManager, **kwargs):
    # TODO ADD CURRENT LESSON TO DB
    dialog_manager.dialog_data["queue_list"] = await pass_queue()
    if dialog_manager.dialog_data.get("current_lesson"):
        return {
            "current_lesson": dialog_manager.dialog_data["current_lesson"],
            "queue_list": dialog_manager.dialog_data.get("queue_list")
        }
    else:
        return {
            "current_lesson": "Нужно выставить пару...",
            "queue_list": dialog_manager.dialog_data.get("queue_list")
        }


async def lessons_getter(**kwargs):
    return {
        "lessons": lessons,
    }
