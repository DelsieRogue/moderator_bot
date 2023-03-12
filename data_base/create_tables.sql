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

drop table if exists publics;
CREATE TABLE publics (
  public_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name_app TEXT NOT NULL,
  name_public TEXT NOT NULL,
  ref_public TEXT NOT NULL,
  n_subsribers INTEGER NOT NULL CHECK (n_subsribers > 0),
  n_views INTEGER NOT NULL CHECK (n_views > 0),
  cost FLOAT NOT NULL CHECK (cost >= 0),
  contact TEXT NOT NULL
);

drop table inactive_subscribes;
CREATE TABLE inactive_subscribes(
  sub_id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER NOT NULL,
  username_1 TEXT NOT NULL,
  username_2 TEXT,
  username_3 TEXT,
  public_id INTEGER NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
  FOREIGN KEY (public_id) REFERENCES publics(public_id)
);

drop table if exists active_subscribes;
CREATE TABLE active_subscribes(
  sub_id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER NOT NULL,
  user_id_1 INTEGER NOT NULL,
  user_id_2 INTEGER,
  user_id_3 INTEGER,
  counter_msg SMALLINT NOT NULL DEFAULT 3,
  public_id INTEGER NOT NULL,
  begin_date datetime NOT NULL DEFAULT (datetime('now', 'localtime')),
  end_date datetime NOT NULL DEFAULT (datetime('now', 'localtime', '+1 month')),
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
  FOREIGN KEY (user_id_1) REFERENCES users(user_id)
  FOREIGN KEY (user_id_2) REFERENCES users(user_id)
  FOREIGN KEY (user_id_3) REFERENCES users(user_id)
  FOREIGN KEY (public_id) REFERENCES publics(public_id)
);