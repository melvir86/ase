DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS card;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS booking;
DROP TABLE IF EXISTS car;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  role TEXT NOT NULL
);

CREATE TABLE card (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  name TEXT NOT NULL,
  number TEXT NOT NULL,
  expiry_month TEXT NOT NULL,
  expiry_year TEXT NOT NULL,
  cve TEXT NOT NULL,
  description TEXT NOT NULL,
  status TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE feedback (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  description TEXT NOT NULL,
  feedback TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE booking (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  car_id INTEGER NULL,
  created TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  source TEXT NOT NULL,
  destination TEXT NOT NULL,
  cost TEXT NOT NULL,
  status TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
  FOREIGN KEY (car_id) REFERENCES car (id)
);

CREATE TABLE car (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  created TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  brand TEXT NOT NULL,
  model TEXT NOT NULL,
  colour TEXT NOT NULL,
  next_service TEXT NOT NULL,
  status TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

-- Preparing sample data before we develop the feature

-- INSERT INTO user (username, password, role) VALUES ('DriverJohn', 'pbkdf2:sha256:600000$D3xjfdhmDCJdqryz$a1d808145d325d04d4f2715be6876f6829065cbeb32a0824e6b3a998758aa3a8', 'Driver');

-- INSERT INTO user (username, password, role) VALUES ('DriverRobert', 'pbkdf2:sha256:600000$aDCwIjzhwoJDCpZ2$7d5f165d9263d450bdc092d2969074b51b030285e734d7955ccb84ed199ebfa1', 'Driver');

-- INSERT INTO user (username, password, role) VALUES ('Mary', 'pbkdf2:sha256:600000$3ZBsWIwwmR8o40VJ$0545998d859e9a967d1bdd0b60076e1a7fe3a3a78e76ec69d1274608341aef12', 'Customer');

INSERT INTO car (user_id, brand, model, colour, next_service, status) VALUES (1, 'Mazda', '3 Hb', 'Red', '23/06/2023', 'Active');

INSERT INTO car (user_id, brand, model, colour, next_service, status) VALUES (2, 'Mazda', '6', 'Blue', '23/12/2023', 'Active');

INSERT INTO booking (user_id, source, destination, cost, status) VALUES (3, 'Wembley Park', 'Euston Square', '$10.50', 'Booked');

INSERT INTO booking (user_id, source, destination, cost, status) VALUES (3, 'Picadilly Circus', 'Goodge Street', '$7.50', 'Booked');