DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS runtime_data;

CREATE TABLE user
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT        NOT NULL,
    identity TEXT        NOT NULL,
    maxgrade INTEGER     NOT NULL
);

CREATE TABLE runtime_data
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    score    INTEGER NOT NULL,
    timeleft INTEGER NOT NULL,
    playing BOOLEAN NOT NULL
);