from aiogram.fsm.state import StatesGroup, State


class PrimaryState(StatesGroup):
    getName = State()
    getFoto = State()
    getLogo = State()
    finishState = State()


class NoDealInBitrix(StatesGroup):
    whereDeal = State()
