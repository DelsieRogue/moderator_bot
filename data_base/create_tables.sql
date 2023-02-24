DROP TABLE if exists users;
CREATE TABLE users(
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR(75) NOT NULL,
  first_name VARCHAR(75),
  last_name VARCHAR(75),
  role_id SMALLINT NOT NULL REFERENCES roles(role_id),
  begin_date DATETIME DEFAULT (datetime('now', 'localtime'))
);

drop table if exists roles;
CREATE table roles(
  role_id INTEGER PRIMARY KEY AUTOINCREMENT,
  role_name VARCHAR(25) NOT NULL UNIQUE
);

INSERT INTO roles(role_name)
VALUES('SUPER_ADMIN'),
('ADMIN'),
('USER'),
('NO_USER');

drop table if exists orders;
create table orders(
  order_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  price FLOAT NOT NULL CHECK (price > 0),
  order_date datetime default (datetime('now', 'localtime')),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

drop table if exists inactive_subscribes;
create table inactive_subscribes(
  sub_id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER NOT NULL,
  username TEXT NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

drop table if exists active_subscribes;
create table active_subscribes(
  sub_id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER NOT NULL,
  user_id_1 INTEGER NOT NULL,
  user_id_2 INTEGER,
  user_id_3 INTEGER,
  counter_msg SMALLINT NOT NULL DEFAULT 3,
  begin_date datetime NOT NULL DEFAULT (datetime('now', 'localtime')),
  end_date datetime NOT NULL DEFAULT (datetime('now', 'localtime', '+1 month')),
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
  FOREIGN KEY (user_id_1) REFERENCES users(user_id)
  FOREIGN KEY (user_id_2) REFERENCES users(user_id)
  FOREIGN KEY (user_id_3) REFERENCES users(user_id)
)