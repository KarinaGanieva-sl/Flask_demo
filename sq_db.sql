CREATE TABLE IF NOT EXISTS mainmenu (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    text TEXT NOT NULL,
    time INTEGER NOT NULL,
    author TEXT,
    FOREIGN KEY (author) REFERENCES user(name)
);

CREATE TABLE IF NOT EXISTS user (
    name TEXT NOT NULL PRIMARY KEY,
    password TEXT NOT NULL
);