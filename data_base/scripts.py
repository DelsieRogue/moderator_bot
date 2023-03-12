import sqlite3
from datetime import datetime as dt

conn = sqlite3.connect("data_base/bot.db")
cur = conn.cursor()


def get_role_name_by_user_id(user_id: int):
    return cur.execute(f"""
    SELECT r.role_name FROM users u 
    LEFT JOIN roles r ON u.role_id=r.role_id
    WHERE u.user_id='{user_id}'""") \
        .fetchone()


def get_users_by_role(role: str) -> list:
    return cur.execute(f"""
        SELECT COALESCE(strftime('%d.%m.%Y', end_date), 'FOREVER') AS 'D', V, P
        FROM (SELECT end_date, u.username AS 'P', u2.username as 'V'  from users u
            LEFT JOIN active_subscribes as2 ON as2.user_id_1=u.user_id 
            LEFT JOIN orders o ON o.order_id=as2.order_id 
            LEFT JOIN users u2 ON u2.user_id=o.user_id
            WHERE u.role_id = (select role_id from roles where role_name = '{role}')
            UNION
            SELECT end_date, u.username AS 'P', u2.username as 'V'  from users u
            LEFT JOIN active_subscribes as2 ON as2.user_id_2=u.user_id 
            LEFT JOIN orders o ON o.order_id =as2.order_id 
            LEFT JOIN users u2 ON o.user_id =u2.user_id 
            WHERE u.role_id = (select role_id from roles where role_name = '{role}')
            UNION
            SELECT end_date, u.username AS 'P', u2.username as 'V'  from users u
            LEFT JOIN active_subscribes as2 ON as2.user_id_3=u.user_id 
            LEFT JOIN orders o ON o.order_id =as2.order_id 
            LEFT JOIN users u2 ON o.user_id =u2.user_id
            WHERE u.role_id = (select role_id from roles where role_name = '{role}')
        )
        ORDER BY D""").fetchall()


def add_user_to_table_users(user_id: int,
                            username: str,
                            role_name: str,
                            fn: str = "",
                            ln: str = ""):
    cur.execute(f"""
    INSERT INTO users (user_id, username, first_name, last_name, role_id)
    VALUES ({user_id}, 
        "{username}", 
        "{fn}", "{ln}",
         (SELECT role_id FROM roles WHERE role_name='{role_name}'));""")
    conn.commit()


def add_order(user_id: int, price: float, count: int) -> int:
    try:
        cur.execute(f"""
        INSERT INTO orders(user_id, price, count_channels)
        VALUES ({user_id}, {price}, {count});""")
        cur.execute('SELECT order_id from orders ORDER BY order_id DESC LIMIT 1')
        conn.commit()
        return cur.fetchone()
    except Exception as ex:
        print(f"[{dt.now(). strftime('%d.%m.%Y %H:%M:%S')}] | ERROR | add_order | EXCEPTION: {ex}")
        return -1


def add_inactive_sub(order_id: int, usernames: dict):
    try:
        cur.execute(f"""
        INSERT INTO inactive_subscribes (order_id, username_1, username_2, username_3)
        VALUES ({order_id}, 
            {"'" + usernames.get(1) + "'" if usernames.get(1) else 'NULL'}, 
            {"'" + usernames.get(2) + "'" if usernames.get(2) else 'NULL'},
            {"'" + usernames.get(3) + "'" if usernames.get(3) else 'NULL'})""")
        conn.commit()
    except Exception as ex:
        print(f"[{dt.now().strftime('%d.%m.%Y %H:%M:%S')}] | ERROR | add_inactive_sub | EXCEPTION: {ex}")


def add_active_sub(order_id: int, user_id: int):
    try:
        cur.execute(f"""
            1""")
    except Exception as ex:
        print(f"[{dt.now().strftime('%d.%m.%Y %H:%M:%S')}] | ERROR | add_active_sub | EXCEPTION: {ex}")


def get_username_by_user_id(user_id: int):
    return cur.execute(f"""
        SELECT u.username FROM users u 
        WHERE u.user_id={user_id}""") \
        .fetchone()[0]
