from aiogram.fsm.state import StatesGroup, State


class PrimaryState(StatesGroup):
    getName = State()
    getFoto = State()
    getLogo = State()
    getLink = State()
    finishState = State()


class NoDealInBitrix(StatesGroup):
    whereDeal = State()
    notDeal = State()
