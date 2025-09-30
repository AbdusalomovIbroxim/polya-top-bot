from aiogram.fsm.state import State, StatesGroup

class RegisterState(StatesGroup):
    fio = State()
    phone = State()
    company = State()
