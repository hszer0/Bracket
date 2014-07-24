__author__ = 'Patrick.Liem'

import unittest
from BracketDB import Database


class BracketTests(unittest.TestCase):

    def setUp(self):
        self.db = Database()

    def test_db_connection(self):
        self.db.c.execute("select name from participants")

    def test_tables(self):
        self.db.c.execute("select name from participants")

    def test_close_db(self):
        self.db.close_connection()
        with self.assertRaises(Exception):
            self.db.c.execute("select name from participants")

    def test_add_and_remove_participant(self):
        #first clear the table
        self.db.c.execute("delete from participants")

        #test for adding
        self.db.add_participant("Patrick")
        self.db.c.execute("select name from participants")
        row = self.db.c.fetchone()
        self.assertEqual("Patrick", row[0])

        #test for removing
        self.db.remove_participant("Patrick")
        self.db.c.execute("select name from participants where name = 'Patrick'")
        self.assertIsNone(self.db.c.fetchone())

