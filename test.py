import unittest
import sqlite3
import time
from FDataBase import FDataBase


class TestFDataBase(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.cur = self.db.cursor()
        self.cur.execute('CREATE TABLE mainmenu (id INTEGER PRIMARY KEY, name TEXT)')
        self.cur.execute('CREATE TABLE posts (id INTEGER PRIMARY KEY, title TEXT, text TEXT, time INTEGER)')

    def tearDown(self):
        self.db.close()

    def test_get_menu(self):
        self.cur.execute("INSERT INTO mainmenu VALUES (1, 'Item 1')")
        self.cur.execute("INSERT INTO mainmenu VALUES (2, 'Item 2')")
        self.db.commit()

        fdb = FDataBase(self.db)
        menu = fdb.get_menu()

        expected_menu = [(1, 'Item 1'), (2, 'Item 2')]
        self.assertEqual(menu, expected_menu)

    def test_add_post(self):
        fdb = FDataBase(self.db)
        fdb.add_post('Test Title', 'Test Text')
        self.cur.execute("SELECT * FROM posts")
        post = self.cur.fetchone()

        expected_post = (1, 'Test Title', 'Test Text', int(time.time()))
        self.assertEqual(post, expected_post)

    def test_get_post(self):
        self.cur.execute("INSERT INTO posts VALUES (1, 'Test Title', 'Test Text', 1234567890)")
        self.db.commit()

        fdb = FDataBase(self.db)
        post = fdb.get_post(1)

        expected_post = ('Test Title', 'Test Text')
        self.assertEqual(post, expected_post)

    def test_get_all_posts(self):
        self.cur.execute("INSERT INTO posts VALUES (1, 'Title 1', 'Text 1', 1234567890)")
        self.cur.execute("INSERT INTO posts VALUES (2, 'Title 2', 'Text 2', 1234567891)")
        self.db.commit()

        fdb = FDataBase(self.db)
        posts = fdb.get_all_posts()

        expected_posts = [(2, 'Title 2', 'Text 2'), (1, 'Title 1', 'Text 1')]
        self.assertEqual(expected_posts, posts)


if __name__ == '__main__':
    unittest.main()
