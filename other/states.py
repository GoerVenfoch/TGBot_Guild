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
    introductionProject = State()
    finishState = State()
