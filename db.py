import sqlite3

conn = sqlite3.connect("user.db", check_same_thread=False)
cursor = conn.cursor()


def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS city (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            city_id INTEGER NOT NULL,
            FOREIGN KEY (city_id) REFERENCES city(id)
        )
    """)
    conn.commit()


def add_cities():
    cities = ["Warsaw", "Krakow", "Gdansk"]

    for city in cities:
        cursor.execute("""
            INSERT INTO city (city_name)
            SELECT ?
            WHERE NOT EXISTS (
                SELECT 1 FROM city WHERE city_name = ?
            )
        """, (city, city))

    conn.commit()


def get_cities():
    cursor.execute("""
        SELECT id, city_name FROM city
    """)
    return cursor.fetchall()


def save_users(chat_id, name, age, city_id):
    cursor.execute("""
        INSERT INTO users (chat_id, name, age, city_id)
        VALUES (?, ?, ?, ?)
    """, (chat_id, name, age, city_id))
    conn.commit()


def get_user_by_chat_id(chat_id):
    cursor.execute("""
        SELECT users.name, users.age, city.city_name
        FROM users
        JOIN city ON users.city_id = city.id
        WHERE users.chat_id = ?
    """, (chat_id,))
    return cursor.fetchone()


def get_user_with_cities():
    cursor.execute("""
        SELECT users.name, users.age, city.city_name
        FROM users
        JOIN city ON users.city_id = city.id
    """)
    return cursor.fetchall()


create_tables()
add_cities()