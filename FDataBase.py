import math
import sqlite3
import time


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Sql Error " + str(e))
        return []

    def add_post(self, title, text, username):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)", (title, text, tm, username))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Sql Error " + str(e))
            return False

    def add_user(self, name, password):
        try:
            self.__cur.execute("INSERT INTO user VALUES(?, ?)", (name, password))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Sql Error " + str(e))
            return False

        return True

    def get_post(self, post_id):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE id = {post_id} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Sql Error " + str(e))

        return False, False

    def is_user_exist(self, name, password):
        try:
            self.__cur.execute(f"SELECT * FROM user WHERE name = {name} and password= {password}")
            res = self.__cur.fetchone()
            if res:
                return True
        except sqlite3.Error as e:
            print("Sql Error " + str(e))

        return False

    def get_all_posts(self):
        try:
            self.__cur.execute(f"SELECT id, title, text FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Sql Error "+str(e))

        return []
