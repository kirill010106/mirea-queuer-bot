from aiogram_dialog import DialogManager
from db.lessons import lessons
from db.dbProcessor import pass_queue, set_lesson_to_table, get_lesson_from_table, get_lessons_list


async def current_lesson_and_queue_getter(dialog_manager: DialogManager, **kwargs):
    current_lesson = await get_lesson_from_table()
    dialog_manager.dialog_data["queue_list"] = await pass_queue()
    if current_lesson:
        return {
            "current_lesson": current_lesson,
            "queue_list": dialog_manager.dialog_data.get("queue_list")
        }
    else:
        return {
            "current_lesson": "Нужно выставить пару...",
            "queue_list": dialog_manager.dialog_data.get("queue_list")
        }


async def lessons_getter(**kwargs):
    return {
        "lessons_list": await get_lessons_list(),
    }
