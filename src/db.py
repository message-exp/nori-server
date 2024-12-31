import sqlite3
from snowflake import SnowflakeGenerator
from datetime import datetime

id_gen = SnowflakeGenerator(1)

def list_to_str(a_list: list) -> str:
    return ",".join(a_list)

def str_to_list(a_string: str) -> list:
    if not a_string:
        return []
    return a_string.split(",")


con = sqlite3.connect('server.db', check_same_thread=False)
cur = con.cursor()

def init_db() -> None:
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, rooms TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS rooms (id INTEGER PRIMARY KEY, room_id TEXT, name TEXT, username TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, target_username TEXT, msg_id TEXT, author_username TEXT, room_id TEXT, message TEXT, timestamp TEXT)")
    con.commit()

def new_user(username: str, password: str) -> None:
    cur.execute("INSERT INTO users (username, password, rooms) VALUES (?, ?, ?)", (username, hash(password), ""))
    con.commit()

def get_user(username: str) -> dict:
    cur.execute("SELECT username, rooms FROM users WHERE username = ?", (username,))
    result = cur.fetchone()
    return {
        "username": result[0] if result else "",
        "rooms": str_to_list(result[1]) if result else []
    }

def generate_room_id() -> str:
    return str(next(id_gen))

def new_room(room_id: str, name: str, usernames: list[str]) -> None:
    cur.execute("INSERT INTO rooms (room_id, name, username) VALUES (?, ?, ?)", (room_id, name, list_to_str(usernames)))
    # add room_id into users table
    for username in usernames:
        cur.execute("SELECT rooms FROM users WHERE username = ?", (username,))
        result = cur.fetchone()
        user_rooms = result[0] if result else ""
        user_rooms = str_to_list(user_rooms)
        user_rooms.append(room_id)
        cur.execute("UPDATE users SET rooms = ? WHERE username = ?", (list_to_str(user_rooms), username))
    con.commit()

def join_room(username: str, room_id: str) -> None:
    # add room_id into users table
    cur.execute("SELECT rooms FROM users WHERE username = ?", (username,))
    result = cur.fetchone()
    user_rooms = result[0] if result else ""
    user_rooms = str_to_list(user_rooms)
    user_rooms.append(room_id)
    cur.execute("UPDATE users SET rooms = ? WHERE username = ?", (list_to_str(user_rooms), username))
    # add username into rooms table
    cur.execute("SELECT username FROM rooms WHERE room_id = ?", (room_id,))
    result = cur.fetchone()
    room_users = result[0] if result else ""
    room_users = str_to_list(room_users)
    room_users.append(username)
    cur.execute("UPDATE rooms SET username = ? WHERE room_id = ?", (list_to_str(room_users), room_id))
    # commit
    con.commit()

def get_room(room_id: str) -> dict:
    cur.execute("SELECT room_id, name, username FROM rooms WHERE room_id = ?", (room_id,))
    result = cur.fetchone()
    return {
        "room_id": result[0] if result else "",
        "name": result[1] if result else "",
        "usernames": str_to_list(result[2]) if result else []
    }

def new_message(author_username: str, room_id: str, message: str, timestamp: datetime) -> None:
    # get room users
    cur.execute("SELECT username FROM rooms WHERE room_id = ?", (room_id,))
    result = cur.fetchone()
    room_users = str_to_list(result[0]) if result else []
    room_users.remove(author_username)

    for target_username in room_users:
        cur.execute(
            "INSERT INTO messages (target_username, msg_id, author_username, room_id, message, timestamp) VALUES (?, ?, ?, ?, ?, ?)", 
            (target_username, next(id_gen), author_username, room_id, message, timestamp.isoformat())
        )
    con.commit()

def get_user_messages(target_username: str) -> list:
    cur.execute("SELECT msg_id, author_username, room_id, message, timestamp FROM messages WHERE target_username = ?", (target_username,))
    result = cur.fetchall()
    messages = [
        {
            "msg_id": row[0],
            "author_username": row[1],
            "room_id": row[2],
            "message": row[3],
            "timestamp": datetime.fromisoformat(row[4])
        }
        for row in result
    ]
    cur.execute("DELETE FROM messages WHERE target_username = ?", (target_username,))
    con.commit()
    return messages
