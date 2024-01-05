from aiogram.dispatcher.filters.state import StatesGroup, State


class UpdateAnket(StatesGroup):
    name = State()
    age = State()
    voice = State()
    confirm = State()


class Home(StatesGroup):
    menu = State()




class Anketa(StatesGroup):
    anketa = State()




class ViewProfiles(StatesGroup):
    warning = State()
    view = State()


class ViewLikes(StatesGroup):
    warning = State()
    view = State()
