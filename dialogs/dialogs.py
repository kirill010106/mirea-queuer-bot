from aiogram_dialog import Dialog, Window, ShowMode
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Select, Column
from aiogram_dialog.widgets.text import Const, Format

from getters.getters import current_lesson_and_queue_getter, lessons_getter
from states.states import UserState
from utils.lessons_kbd_generator import lessons_kbd
from utils.add_to_queue import add_to_queue
from db.dbProcessor import clear_queue, pass_queue, remove_from_queue_output
from utils.password_checker import is_password_correct
from utils.reload_window import reload_window
main_dialog = Dialog(
    Window(
        Const("Добро пожаловать в QueuerBot"),
        Format("Сейчас идет пара {current_lesson}"),
        Const("Текущая очередь:"),
        # TODO List
        # Button(Const("Вывести очередь"), on_click=pass_queue, id="pass_queue_btn"),
        Format("{queue_list}"),
        SwitchTo(Const("Обновить очередь"), id="reload_button", state=UserState.main, show_mode=ShowMode.EDIT),
        SwitchTo(Const("Записаться"), id="check_in_btn", state=UserState.checkIn_confirmation),
        SwitchTo(Const("Покинуть очередь"), id="check_out_btn", state=UserState.checkOut_confirmation),
        SwitchTo(Const("Поменять пару [Требуется ввод пароля]"), id="choose_lesson", state=UserState.password_enter),
        getter=current_lesson_and_queue_getter,
        state=UserState.main,
    ),
    Window(
        Const("Бот был перезапущен. Для возврата в главное меню воспользуйтесь кнопкой."),
        SwitchTo(Const("Перейти в главное меню"), state=UserState.main, id="back"),
        state=UserState.reload
    ),

    Window(
        Format("Подтвердите запись на ответ на паре {current_lesson}:"),
        Button(Const("Подтвердить"), id="confirm", on_click=add_to_queue),
        SwitchTo(Const("Вернуться"), id="back", state=UserState.main),
        getter=current_lesson_and_queue_getter,
        state=UserState.checkIn_confirmation,
    ),
    Window(
        Format("Подтвердите отмену записи на паре {current_lesson}:"),
        Const("Вы потеряете место в очереди!"),
        Button(Const("Подтвердить"), id="confirm", on_click=remove_from_queue_output),
        SwitchTo(Const("Вернуться"), id="back", state=UserState.main),
        state=UserState.checkOut_confirmation,
        getter=current_lesson_and_queue_getter,
    ),
    Window(
        Const("Введите пароль: "),
        MessageInput(is_password_correct),
        SwitchTo(Const("Назад"), state=UserState.main, id="back", show_mode=ShowMode.DELETE_AND_SEND),
        state=UserState.password_enter,
    ),
    Window(
        Const("Выберите новую пару для записи:"),
        Const("ВНИМАНИЕ, вся прошлая запись будет сброшена!"),
        Column(
            lessons_kbd,
        ),
        # SwitchTo(Const("[Выбрать]"), state=UserState.lesson_confirmation, id="lesson_choose"),
        SwitchTo(Const("Вернуться"), id="back", state=UserState.main),
        state=UserState.choose_lesson,
        getter=lessons_getter,
    ),
    Window(
        Format("Точно меняем пару на []?"),
        Button(Const("Да"), id="confirm"),
        SwitchTo(Const("Вернуться"), state=UserState.main, id="back"),
        state=UserState.lesson_confirmation,
    )
)
