DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS runtime_data;
DROP TABLE IF EXISTS talents;
DROP TABLE IF EXISTS mistake;

CREATE TABLE user
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT        NOT NULL,
    identity TEXT        NOT NULL,
    maxgrade INTEGER     NOT NULL,
    talent_id INTEGER    NOT NULL
);

CREATE TABLE runtime_data
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    score    INTEGER NOT NULL,
    timeleft INTEGER NOT NULL,
    currenttime INTEGER NOT NULL
);

CREATE TABLE talents
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    prevent_death INTEGER NOT NULL,
    blessed INTEGER NOT NULL
);

CREATE TABLE mistake
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    error_times INTEGER NOT NULL,
    content TEXT NOT NULL
)