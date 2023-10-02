from aiogram.fsm.state import StatesGroup, State


class PrimaryState(StatesGroup):
    getName = State()
    connectChatGuild = State()
    acquaintance = State()
    getFoto = State()
    getLogo = State()
    connectPortal = State()
    introductionGuild = State()
    look_points = State()
    introductionRegulation = State()
    introductionShildic = State()
    introductionProject = State()
    finishState = State()


class NoDealInBitrix(StatesGroup):
    whereDeal = State()
