from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    main = State()
    choose_lesson = State()
    lesson_confirmation = State()
    password_enter = State()
    queue = State()
    checkIn_confirmation = State()
    checkOut_confirmation = State()
    reload = State()
