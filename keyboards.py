from aiogram import types


async def cancel():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Отмена'))
    return keyboard


async def delete():
    keyboard = types.ReplyKeyboardRemove()
    return keyboard


async def back():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Назад'))
    return keyboard


async def start():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Главная'),
                 types.KeyboardButton('На пончик'))
    return keyboard


async def reaction():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('❤️'),
                 types.KeyboardButton('Следующая анкета'),
                 types.KeyboardButton('Главная'))
    return keyboard


async def save():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Сохранить'),
                 types.KeyboardButton('Отмена'))
    return keyboard


async def start():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Главная'),
                 types.KeyboardButton('Другие боты'))
    return keyboard


async def home_btn():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Главная'))
    return keyboard


async def home():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Моя анкета'),
                 types.KeyboardButton('Слушать'),
                 types.KeyboardButton('Отключить мою анкету'))
    return keyboard


async def anketa():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Изменить анкету'),
                 types.KeyboardButton('Назад'))
    return keyboard


async def update_anket():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Изменить анкету'),
                 types.KeyboardButton('Отмена'))
    return keyboard


async def new_anket():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Создать анкету'))
    return keyboard


async def kb_12():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('1'), types.KeyboardButton('2'))
    return keyboard


async def kb_10():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('1'), types.KeyboardButton('0'))
    return keyboard


async def kb_1234():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('1'), types.KeyboardButton('2'),
                 types.KeyboardButton('3'), types.KeyboardButton('4'))
    return keyboard


async def profile_view():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('❤️'), types.KeyboardButton('👎'), types.KeyboardButton('💤'))
    return keyboard


async def profile_warning():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Продолжить'))
    return keyboard


async def likers_view():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('❤️'), types.KeyboardButton('👎'), types.KeyboardButton('💤'))
    return keyboard
