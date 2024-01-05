import sqlite3 as sq
from aiogram import types
from main import bot


async def ads_id(id) -> None:
    db1 = sq.connect("id_start.db")
    cur1 = db1.cursor()
    cur1.execute(
        'CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY UNIQUE ON CONFLICT IGNORE)'
    )
    cur1.execute('SELECT COUNT(*) FROM users WHERE id = ?', (id,))
    result = cur1.fetchone()[0]

    if result == 0:
        # Если записи с заданным id нет, то добавляем ее
        cur1.execute('INSERT INTO users (id ) VALUES (?)', (id,))
        db1.commit()
        print(f'Новая запись с id {id} добавлена')
    db1.commit()


async def db_connect() -> None:
    global db, cur
    db = sq.connect("new9.db")
    cur = db.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY UNIQUE ON CONFLICT IGNORE,\
         name TEXT, voice TEXT, age TEXT, username TEXT, active TEXT, date TEXT,\
          profile_likes TEXT)'
    )
    db.commit()


async def add_column(name):
    query = f"ALTER TABLE users ADD COLUMN {name} TEXT"
    cur.execute(query)
    db.commit()


async def get_user(id) -> list:
    cur.execute("SELECT * FROM users WHERE id=?", (id,))
    user = cur.fetchone()
    print(cur.fetchall())
    db.commit()
    return user


async def get_users():
    users = cur.execute("SELECT * FROM users").fetchall()
    return users


async def del_user(id):
    sql_update_query = """DELETE from users where id = ?"""
    cur.execute(sql_update_query, (id,))


async def check_id(id):
    cur.execute("SELECT * FROM users WHERE id=?", (id,))
    row = cur.fetchone()
    print(row, " chek_id если нон то фолз")
    if row is None:
        return False
    db.commit()
    return True


async def active(id_user, on=1):
    if on == 1:
        cur.execute('UPDATE users SET active=? WHERE id=?', (on, id_user))
        db.commit()
        return 'active = 1'
    if on == 0:
        cur.execute('UPDATE users SET active=? WHERE id=?', (on, id_user))
        db.commit()
        return "active 0"

    else:
        return 'Ничего не сделал'


async def get_likers(id):
    profile = await get_user(id)

    if (profile is None) or (profile[7] is None):
        return None
    if ' ' in profile[7]:
        likers = profile[7].split(' ')
    else:
        likers = [profile[7]]
    return likers


async def add_like(liker_message: types.Message, id):
    liker = str(liker_message.from_user.id)
    cur.execute('SELECT profile_likes FROM users WHERE id = ?', (id,))
    result = cur.fetchone()
    print(result[0])
    if result[0] is None:
        liker = f"{liker}"
        cur.execute('UPDATE users SET profile_likes=? WHERE id=?', (liker, id))
    elif liker not in result[0]:
        liker = f"{result[0]} {liker}"
        cur.execute('UPDATE users SET profile_likes=? WHERE id=?', (liker, id))
    cur.execute('SELECT profile_likes FROM users WHERE id = ?', (id,))
    like_count = len(cur.fetchone()[0].split(' '))
    await bot.send_message(id,
                           f"Кому-то понравилась ваша анкета.  ({like_count})\nЧтобы увидеть кто это, перейдите в раздел /my_likers")
    db.commit()


# Вроде мусор - не помню зачем добавил set_like
async def set_like(new_likers, id):
    # new_likers сама строка с лайкерами
    # id у кого ставим новый список лайкеров
    new_likers = str(new_likers)
    cur.execute('UPDATE users SET profile_likes=? WHERE id=?', (new_likers, id))


async def del_like(id, liker):
    # Удаляет у пользователя с таким id симпатию с таким liker
    cur.execute('SELECT profile_likes FROM users WHERE id = ?', (id,))
    result = cur.fetchone()
    print(result[0])
    if result[0] is None:
        pass
    elif liker in result[0]:
        likers = result[0].split(' ') # для определения количества симпатий пользователя
        likers_str = result[0]
        if len(likers) == 1:
            likers_str = None
        elif likers[0] == str(liker): # если симпатия стоит на первом месте, то делаем так чтобы правильно убрать пробелы в строке на которую хотим заменить
            likers_str = likers_str.replace(f'{liker} ', '')
        else:
            likers_str = likers_str.replace(f' {liker}', '')

        cur.execute('UPDATE users SET profile_likes=? WHERE id=?', (likers_str, id))


async def add_id(id):
    # Выбрать данные с указанным id
    # эта функция Нужна только в функции update!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    cur.execute('SELECT COUNT(*) FROM users WHERE id = ?', (id,))  # №№№№№№№№№№№№№fhmfmjtjytrevtrbrrrrrrrrrrrrrrrrr
    result = cur.fetchone()[0]

    if result == 0:
        # Если записи с заданным id нет, то добавляем ее
        cur.execute('INSERT INTO users (id ) VALUES (?)', (id,))
        cur.execute('UPDATE users SET active=? WHERE id=?', ("1", id))
        db.commit()
        print(f'Новая запись с id {id} добавлена')

    db.commit()


async def update(user):
    id = user[0]
    name = user[1]
    voice = user[2]
    age = user[3]
    username = f'@{user[4]}'
    date = user[5]
    active = "1"
    await add_id(id)
    cur.execute("UPDATE users SET name=?, voice=?, age=?, username=?, active=?, date=? WHERE id=?",
                (name, voice, age, username, active, date, id))
    db.commit()


def get_filtered_date(age):
    # Select rows from the database in the required order
    cur.execute(
        "SELECT * FROM users ORDER BY CAST(date AS INTEGER) DESC, ABS(CAST(age AS INTEGER) - ?) ASC, CAST(age AS INTEGER) ASC",
        (age,))

    rows = cur.fetchall()
    db.commit()
    return rows


def get_filtered_users(age: str):
    age = int(age)
    # Select rows from the database in the required order
    cur.execute(f"SELECT * FROM users WHERE age >= {age - 2} ORDER BY age ASC, date DESC")

    rows = cur.fetchall()
    db.commit()
    return rows


"""query = f"SELECT * FROM your_table WHERE age BETWEEN {age-2} AND {age+2} ORDER BY date DESC, age ASC"
    cursor.execute(query)"""

# ################################################################################
# #######################           ##################################################
# #######################   trash   #########################################################
# #######################           ##################################################
# ################################################################################
"""
async def add_user(user_bio: list):
    id = user_bio[0]
    name = user_bio[1]
    audio = user_bio[2]
    age = user_bio[3]
    username = f'@{user_bio[4]}'
    user = cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)",
                       (id, name, audio, age, username))
    db.commit()
    print('Успешно сохранено')
    return user


# async def get_ankets(age):
async def add_id(id):
    # Выбрать данные с указанным id

    cur.execute('SELECT COUNT(*) FROM users WHERE id = ?', (id,))  # №№№№№№№№№№№№№fhmfmjtjytrevtrbrrrrrrrrrrrrrrrrr
    result = cur.fetchone()[0]

    if result == 0:
        # Если записи с заданным id нет, то добавляем ее
        cur.execute('INSERT INTO users (id ) VALUES (?)', (id,))
        cur.execute('UPDATE users SET active=? WHERE id=?', ("1", id))
        db.commit()
        print(f'Новая запись с id {id} добавлена')

    db.commit()
"""
