import sqlite3


conn = sqlite3.connect("data_base/bot.db")
cur = conn.cursor()


def get_role_name(user_id):
    return cur.execute(
        f"""SELECT r.role_name FROM users u LEFT JOIN roles r ON u.role_id=r.role_id WHERE u.user_id='{user_id}'""") \
        .fetchone()


def get_users_from_db(roles):
    roles_for_query = str(roles)[1:-1]
    return cur.execute(f"""SELECT u.username, strftime('%d.%m.%Y', max(s.end_date)) FROM users u
                    LEFT JOIN roles  r ON u.role_id=r.role_id LEFT JOIN active_subscribes s ON u.user_id =s.user_id_1
                    LEFT JOIN orders o ON s.order_id = o.order_id
                    WHERE r.role_name IN ({roles_for_query}) GROUP BY u.username""").fetchall()


def add_user_to_table_users(user_id, username, role_name, fn="", ln=""):
    cur.execute(f"""SELECT role_id FROM roles WHERE role_name="{role_name}" """)
    res = cur.fetchone()[0]
    cur.execute(f"""INSERT INTO users (user_id, username, first_name, last_name, role_id)
     VALUES ({user_id}, "{username}", "{fn}", "{ln}", {res});""")
    conn.commit()
