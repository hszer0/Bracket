__author__ = 'Patrick.Liem'

import unittest
from BracketDB import Database


class BracketTests(unittest.TestCase):

    def setUp(self):
        self.db = Database()

    def tearDown(self):
        self.db.close_connection()

    def test_tables_and_columns(self):
        self.db.c.execute("select name from participants")
        self.db.c.execute("select id, name, date from tournaments")
        self.db.c.execute("select tid, name from contenders")
        self.db.c.execute("select tid, round, name1, name2, score1, score2 from scores")

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
        self.db.c.execute("select name from participants")
        self.assertIsNone(self.db.c.fetchone())

    def test_add_and_remove_tournament(self):
        #first clear the table
        self.db.c.execute("delete from tournaments")

        #test for adding
        tid = self.db.add_tournament("UT2k4", "2014-01-01")
        self.db.c.execute("select name, date from tournaments")
        row = self.db.c.fetchone()
        self.assertEqual(("UT2k4", "2014-01-01"), row)

        #test for removing
        self.db.remove_tournament(tid)
        self.db.c.execute("select id from tournaments")
        self.assertIsNone(self.db.c.fetchone())

    def test_add_and_remove_contender(self):
        #first clear the table
        self.db.c.execute("delete from contenders")

        #test for adding
        tid = self.db.add_tournament("UT2k4", "2014-01-01")
        self.db.add_contender(tid, "Patrick")
        self.db.c.execute("select tid, name from contenders")
        row = self.db.c.fetchone()
        self.assertEqual((tid, "Patrick"), row)

        #test for removing
        self.db.remove_contender(tid, "Patrick")
        self.db.remove_tournament(tid)
        self.db.c.execute("select * from contenders")
        self.assertIsNone(self.db.c.fetchone())


