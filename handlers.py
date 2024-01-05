import asyncio
import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher
import keyboards as kb
import filter
import sq_bd
from config import admin_list
from main import bot, dp
from states import Home, UpdateAnket, Anketa, ViewProfiles, ViewLikes
import re
import json
from filter import get_date


async def wait(time):
    await asyncio.sleep(time)


async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_list[0], text="Bot is started")
    await sq_bd.db_connect()
    await bot.send_message(chat_id=admin_list[0], text="БД подключена")


####################################################################################### handlers ##################

@dp.message_handler(commands=['users'], state="*")
async def get_users_handler(message: types.Message, state: FSMContext):
    await message.answer(f"{await sq_bd.get_users()}")
    rows = sq_bd.get_filtered_date(15)
    rows2 = sq_bd.get_filtered_users("15")
    await message.answer(f"{rows}")
    await message.answer(f"{rows2}")


@dp.message_handler(commands=['test'], state="*")
async def get_users_handler(message: types.Message, state: FSMContext):
    await sq_bd.add_like(message, message.from_user.id)
    msg = await message.answer(f'<a href="tg://user?id={message.from_user.id}">qwertyui</a>')
    msg2 = await message.answer(f'href="tg://user?id={message.from_user.id}"')
    msg3 = await message.answer(f'<a href="tg://openmessage?user_id={5988050571}">qwertyui</a>')
    button_url = f'tg://openmessage?user_id={5988050571}'
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='button_text', url=button_url))
    await message.answer('123', reply_markup=markup)
    print(msg)


@dp.message_handler(commands=['add_column'], state="*")
async def add_column_handler(message: types.Message, state: FSMContext):
    text = message.text.split(' ')
    if len(text) == 1:
        return None
    arg = text[1]
    await sq_bd.add_column(arg)


@dp.message_handler(commands=['message'], state="*")
async def json_message(message: types.Message, state: FSMContext):
    data = json.loads(f"{message}")
    # Красиво форматируем JSON с использованием отступов
    pretty_json = json.dumps(data, indent=6, ensure_ascii=False)
    text = pretty_json
    await bot.send_message(admin_list[0], text=text)
    await bot.send_message(admin_list[0], text=f"{await get_date(message)}")


@dp.message_handler(commands=['users_count'], state="*")
async def users_count(message: types.Message, state: FSMContext):
    await message.answer(f"{len(await sq_bd.get_users())}")


@dp.message_handler(commands=['start'], state="*")
async def start_handler(message: types.Message, state: FSMContext):
    await sq_bd.ads_id(message.from_user.id)
    if (await state.get_state()) is not None:
        await state.finish()

    text = f"""Добро пожаловать в бота со звуком\n/home - Главная\n/my_profile - Твоя анкета\n\n <a href="tg://user?id={message.from_user.id}">Твой профиль</a>"""
    await message.answer(text=text, reply_markup=await kb.start())


@dp.message_handler(lambda message: message.text in ['Назад', 'Главная', 'Отмена'], state="*")
async def home(message: types.Message, state: FSMContext):
    if message.text == '💤':
        await message.answer("Подождем, пока твою кто-то не услышит твой голос")
    await state.finish()
    await message.answer('Главная', reply_markup=await kb.home())
    await Home.menu.set()


async def anketa(message: types.Message, state: FSMContext):
    await message.answer('Твоя анкета')
    if await sq_bd.check_id(message.from_user.id):
        user_data = await sq_bd.get_user(message.from_user.id)
        caption = f"{user_data[1]}, {user_data[3]}"
        voice = user_data[2]
        await message.answer_voice(voice=voice, caption=caption, reply_markup=await kb.anketa())
    else:
        await message.answer('Хм... Тут пусто, нажми на "Изменить анкету" для того чтобы создать анкету',
                             reply_markup=await kb.anketa())
    await state.set_state(Anketa.anketa.set)
    await Anketa.anketa.set()


async def Update_anketa_1(message: types.Message, state: FSMContext):
    await message.answer('Как тебя называть?', reply_markup=await kb.cancel())
    await UpdateAnket.name.set()


async def Update_anketa_2(message: types.Message, state: FSMContext):
    text = filter.remove_tags(filter.remove_html_tags(message.text))
    await state.update_data(name=text)
    await message.answer('Введи свой возраст', reply_markup=await kb.cancel())
    await UpdateAnket.age.set()


async def Update_anketa_3(message: types.Message, state: FSMContext):
    if re.match("^\d\d$", message.text):
        if 10 < int(message.text) < 36:
            await state.update_data(age=message.text)
        else:
            return await message.answer("Введи свой возраст. (11-35)")
    else:
        return await message.answer("Введи свой возраст. (11-35)")
    await message.answer('Отправь свой гс', reply_markup=await kb.cancel())
    await UpdateAnket.voice.set()


async def Update_anketa_4(message: types.Message, state: FSMContext):
    await state.update_data(voice=message.voice.file_id)
    user_data = await state.get_data()
    name = user_data.get("name")
    age = user_data["age"]
    voice = user_data["voice"]
    await message.answer_voice(voice, caption=f"<b>{name}</b>, {age}")
    await message.answer('Все верно?', reply_markup=await kb.save())
    await UpdateAnket.confirm.set()


async def save_anketa(message: types.Message, state: FSMContext):
    await message.answer("Сохранено")
    # Сохранение в бд
    id = message.from_user.id
    name = (await state.get_data('name')).get('name')
    voice = (await state.get_data('voice')).get('voice')
    age = (await state.get_data('age')).get('age')
    username = message.from_user.username
    date = await get_date(message)
    user_data = [id, name, voice, age, username, date]
    await sq_bd.update(user_data)
    await state.finish()  # Очищает данные с состояния и выходит с состояния
    await message.answer('Главная', reply_markup=await kb.home())
    await Home.menu.set()  # Снова задает состояние


################################################################################################# OFF ANKET ####################


async def off_anketa(message: types.Message, state: FSMContext):
    await message.answer("Ошибка конфиденциальности")
    # Переключение состояния анкеты в бд на 0 или False
    await message.answer('Главная', reply_markup=await kb.home())
    await Home.menu.set()  # Снова задает состояние


# ############################################################  Profile View  #########
async def own_profile(state, message):
    user_data = await state.get_data()
    profile = user_data["profiles"][user_data["profile_num"]]
    profile_id = int(profile[0])
    return message.from_user.id == profile_id


async def check_last_profile(state, message):
    user_data = await state.get_data()
    if user_data["profile_num"] == (user_data["profiles_count"]):
        if message.text == '❤️':
            liked_profile = user_data["profiles"][user_data["profile_num"] - 1][0]
            await sq_bd.add_like(message, liked_profile)
            await message.answer("Лайк отправлен")
        await message.answer("К сожалению, пока новых анкет нет, возвращайтесь позже!")
        await message.answer("Главная", reply_markup=await kb.home())
        return True
    return False


async def profile_view_warning(message: types.Message, state: FSMContext):
    text = """❗️ Помни, что в интернете люди могут выдавать себя за других.
Бот не запрашивает личные данные и не идентифицирует пользователей по паспортным данным. 
 
 Продолжая использование бота ты соглашаешься с использованием бота на свой страх и риск."""

    if await sq_bd.check_id(message.from_user.id):
        await state.finish()
        age = (await sq_bd.get_user(message.from_user.id))[3]
        profiles = sq_bd.get_filtered_users(age=age)
        profiles_count = len(profiles)
        random.shuffle(profiles) # Зарандомил список пользователей чтобы при каждом запуске попадались рандомы. Мне лень делать норм список, чтобы для каждого отдельного пользователя запоминать, что он смотрел, что нет)
        print(profiles)
        await state.update_data(profiles=profiles)
        await state.update_data(profiles_count=profiles_count)
        await state.update_data(profile_num=0)
        await message.answer(text=text, reply_markup=await kb.profile_warning())
        await ViewProfiles.view.set()
    else:
        await message.answer('Чтобы продолжить, тебе надо создать анкету - нажми на кнопку "Изменить анкету"',
                             reply_markup=await kb.anketa())
        await Anketa.anketa.set()


async def profile_view(message: types.Message, state: FSMContext):
    if await check_last_profile(state, message):
        return await Home.menu.set()
    user_data = await state.get_data()
    if message.text == '❤️':
        liked_profile = user_data["profiles"][user_data["profile_num"] - 1][0]
        await sq_bd.add_like(message, liked_profile)  # Добавляем лайк автору профиля
        await message.answer("Лайк отправлен")
        if await own_profile(state, message):
            profiles_num = user_data["profile_num"] + 1
            await state.update_data(profile_num=profiles_num)
            return await message.answer("Подпишись на канал ", reply_markup=await kb.profile_warning())
        profile = user_data["profiles"][user_data["profile_num"]]
        profile_id, profile_name, profile_voice, profile_age = profile[0], profile[1], profile[2], profile[3]
        caption = f"{profile_name}, {profile_age}\n\n<b>@bot_username</b>"
        await message.answer_voice(voice=profile_voice, caption=caption, reply_markup=await kb.profile_view())
    elif message.text == '👎':
        if await own_profile(state, message):
            profiles_num = user_data["profile_num"] + 1
            await state.update_data(profile_num=profiles_num)
            return await message.answer("Подпишись на канал ", reply_markup=await kb.profile_warning())
        profile = user_data["profiles"][user_data["profile_num"]]
        profile_id, profile_name, profile_voice, profile_age = profile[0], profile[1], profile[2], profile[3]
        caption = f"{profile_name}, {profile_age}\n\n<b>@bot_username</b>"
        await message.answer_voice(voice=profile_voice, caption=caption, reply_markup=await kb.profile_view())
    elif message.text == 'Продолжить':
        if await own_profile(state, message):
            profiles_num = user_data["profile_num"] + 1
            await state.update_data(profile_num=profiles_num)
            return await message.answer("Подпишись на канал ", reply_markup=await kb.profile_warning())
        profile = user_data["profiles"][user_data["profile_num"]]
        profile_id, profile_name, profile_voice, profile_age = profile[0], profile[1], profile[2], profile[3]
        caption = f"{profile_name}, {profile_age}\n\n<b>@bot_username</b>"
        await message.answer_voice(voice=profile_voice, caption=caption, reply_markup=await kb.profile_view())
    profiles_num = user_data["profile_num"] + 1
    await state.update_data(profile_num=profiles_num)

    print(user_data["profile_num"])


# ############################################################  Likes View  #########


async def likes_view_warning(message: types.Message, state: FSMContext):
    likers = await sq_bd.get_likers(message.from_user.id)
    if not await sq_bd.check_id(message.from_user.id):
        await Home.menu.set()
        await message.answer("Сначала создай свою анкету")
        return await message.answer("<b>Главная</b>", reply_markup=await kb.home())
    if (likers is None) or (likers == 'None'):
        await Home.menu.set()
        await message.answer("Пока лайков нет, загляни позже")
        return await message.answer("<b>Главная</b>", reply_markup=await kb.home())
    if True: print(
        "Подпишись на канал, чтобы продолжить")  # Тут может быть действие, если юзер не подписан на канал какой-нибудь
    await ViewLikes.warning.set()
    await state.update_data(likers=likers)
    await state.update_data(likers_count=len(likers))

    text = """❗️ Помни, что в интернете люди могут выдавать себя за других.
Бот не запрашивает личные данные и не идентифицирует пользователей по паспортным данным. 
 
 Продолжая использование бота ты соглашаешься с использованием бота на свой страх и риск."""
    await message.answer(text=text, reply_markup=await kb.profile_warning())


async def likes_view(message: types.Message, state: FSMContext):
    await ViewLikes.view.set()
    user_data = await state.get_data()
    likers = user_data["likers"]
    print(likers)

    if (likers is None) or (likers == 'None'):
        if message.text == '❤️':
            print("Первый случай лайка")
            own_profile_name = (await sq_bd.get_user(message.from_user.id))[1]
            last_profile_id, last_profile_name = user_data["previous_liker"]
            await sq_bd.del_like(message.from_user.id, last_profile_id)
            # Отправляет ссылку тому, кто первый лайкнул
            await bot.send_message(last_profile_id,
                                   f'Есть взаимная симпатия: <a href="tg://openmessage?user_id={message.from_user.id}">{own_profile_name}</a>')
            # Отправляет ссылку тому, кто одобрил симпатию
            await message.answer(
                f'Отлично! Надеюсь хорошо проведете время😊\nНачинай общаться👉 <a href="tg://openmessage?user_id={last_profile_id}">{last_profile_name}</a>')
        elif message.text == '👎':
            print("Первый случай дизлайка")
            own_profile_name = (await sq_bd.get_user(message.from_user.id))[1]
            last_profile_id, last_profile_name = user_data["previous_liker"]
            await sq_bd.del_like(message.from_user.id, last_profile_id)
        await message.answer("Все лайки просмотрены")
        await message.answer("<b>Главная</b>", reply_markup=await kb.home())
        return await Home.menu.set()

    profile = await sq_bd.get_user(likers[0])
    profile_id, profile_name, profile_voice, profile_age = profile[0], profile[1], profile[2], profile[3]
    await sq_bd.del_like(message.from_user.id, profile_id)
    if message.text == 'Продолжить':
        if len(likers) == 1:
            likers = None
        else:
            likers = likers[1:]
        await state.update_data(likers=likers)
        caption = f"Есть симпатия:\n\n{profile_name}, {profile_age}"
        await state.update_data(previous_liker=(profile_id, profile_name))
        return await message.answer_voice(voice=profile_voice, caption=caption, reply_markup=await kb.likers_view())

    elif message.text == '❤️':
        if len(likers) == 1:
            likers = None
        else:
            likers = likers[1:]
        await state.update_data(likers=likers)
        own_profile_name = (await sq_bd.get_user(message.from_user.id))[1]
        user_data = await state.get_data()
        last_profile_id, last_profile_name = user_data["previous_liker"]
        await bot.send_message(last_profile_id,
                               f'Есть взаимная симпатия!\nСсылка для мобильных устройств: <a '
                               f'href="tg://openmessage?user_id={message.from_user.id}">{own_profile_name}</a>')
        await message.answer(
            f'Отлично! Надеюсь хорошо проведете время😊\nНачинай общаться, вот ссылка для мобильных устройств👉<a '
            f'href="tg://openmessage?user_id={last_profile_id}">{last_profile_name}</a>')
        caption = f"Есть симпатия:\n\n{profile_name}, {profile_age}"
        await state.update_data(previous_liker=(profile_id, profile_name))
        return await message.answer_voice(voice=profile_voice, caption=caption, reply_markup=await kb.likers_view())
    elif message.text == '👎':
        if len(likers) == 1:
            likers = None
        else:
            likers = likers[1:]
        await state.update_data(likers=likers)
        caption = f"Есть симпатия:\n\n{profile_name}, {profile_age}"
        await state.update_data(previous_liker=(profile_id, profile_name))
        return await message.answer_voice(voice=profile_voice, caption=caption, reply_markup=await kb.likers_view())
    elif message.text == '💤':
        await Home.menu.set()
        return await message.answer("<b>Главная</b>", reply_markup=await kb.home())


# ################################################################################################# REGISTRATORS #######################
# Хотел регистраторы в другой файл перекинуть, не знаю, сработает ли


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(home, commands="home", state="*")
    dp.register_message_handler(anketa, commands="my_profile", state="*")
    dp.register_message_handler(anketa, Text(equals="Моя анкета", ignore_case=True), state="*")
    dp.register_message_handler(off_anketa, Text(equals="Отключить мою анкету", ignore_case=True), state=Home.menu)
    dp.register_message_handler(off_anketa, commands="off_anket", state=Home.menu)


def register_updateAnket_handlers(dp: Dispatcher):
    dp.register_message_handler(home, Text(contains=["Назад", "Отмена", "0"], ignore_case=True), state="*")
    dp.register_message_handler(Update_anketa_1,
                                Text(equals="Изменить анкету", ignore_case=True), state=Anketa.anketa)
    dp.register_message_handler(Update_anketa_2, state=UpdateAnket.name)
    dp.register_message_handler(Update_anketa_3, state=UpdateAnket.age)
    dp.register_message_handler(Update_anketa_4, content_types=types.ContentType.VOICE, state=UpdateAnket.voice)
    dp.register_message_handler(save_anketa, Text(equals="Сохранить"), state=UpdateAnket.confirm)


def register_ProfileView(dp: Dispatcher):
    dp.register_message_handler(profile_view_warning, Text(equals="Слушать", ignore_case=True), state="*")
    dp.register_message_handler(profile_view, Text(equals="❤️"), state=ViewProfiles.view)
    dp.register_message_handler(profile_view, Text(equals='👎'), state=ViewProfiles.view)
    dp.register_message_handler(home, Text(equals='💤'), state=ViewProfiles.view)
    dp.register_message_handler(profile_view, Text(equals="Продолжить"), state=ViewProfiles.view)


def register_LikersView(dp: Dispatcher):
    dp.register_message_handler(likes_view_warning, Text(equals="Симпатии", ignore_case=True), state=Home.menu)
    dp.register_message_handler(likes_view_warning, commands=['my_likers'], state='*')
    dp.register_message_handler(likes_view, Text(equals="Продолжить", ignore_case=True), state=ViewLikes.warning)
    dp.register_message_handler(likes_view, Text(equals="❤️"), state=ViewLikes.view)
    dp.register_message_handler(likes_view, Text(equals='👎'), state=ViewLikes.view)
    dp.register_message_handler(home, Text(equals='💤'), state=ViewLikes.view)


def newStart(dp: Dispatcher):
    dp.register_message_handler(home, Text(equals="❤️"), state='*')
    dp.register_message_handler(home, Text(equals='👎'), state='*')
    dp.register_message_handler(home, Text(equals='💤'), state='*')
    dp.register_message_handler(home, Text(equals="Продолжить", ignore_case=True), state='*')

register_LikersView(dp)
register_updateAnket_handlers(dp)
register_handlers(dp)
register_ProfileView(dp)

# newStart Всегда в конце, так как это на случай перезапуска бота, когда сбросятся состояния. Если будет выше других,
# то кнопки не будут правильно работать, а просто возвращать на главную.
newStart(dp)