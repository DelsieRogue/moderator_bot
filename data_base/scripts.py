import sqlite3

conn = sqlite3.connect("data_base/bot.db")
cur = conn.cursor()


def get_role_name(user_id: int):
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
         (SELECT role_id FROM roles WHERE role_name="{role_name}"));""")
    conn.commit()
