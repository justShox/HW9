import sqlite3

connection = sqlite3.connect('Weather', check_same_thread=False)
cursor = connection.cursor()

# Создаем таблицу
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT, phone_number TEXT, location TEXT);")


def registration(id, name, phone_number, location):
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
                   (id, name, phone_number, location))
    connection.commit()


def checker(id):
    check = cursor.execute("SELECT id FROM users WHERE id = ?", (id,))
    if check.fetchone():
        return True
    else:
        return False
