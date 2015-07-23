import unittest
from BracketDB import Database
#from BracketControl import Bcontrol


class BracketDBTests(unittest.TestCase):

    def setUp(self):
        self.db = Database("test.db")
        self.db.add_participant("Patrick")
        self.db.add_participant("Steven")
        self.db.add_participant("Simone")
        self.db.add_participant("Anke")
        tid = self.db.add_tournament("Unreal", "2014-01-01")
        self.db.add_contender(tid, "Patrick")
        self.db.add_contender(tid, "Steven")
        self.db.add_contender(tid, "Simone")
        self.db.add_contender(tid, "Anke")
        self.db.add_game(tid, 0, "Patrick", "Simone")
        self.db.add_game(tid, 0, "Steven", "Anke")

    def tearDown(self):
        self.db.c.execute("delete from participants")
        self.db.c.execute("delete from tournaments")
        self.db.c.execute("delete from contenders")
        self.db.c.execute("delete from scores")
        self.db.close_connection()

#    def test_switch_contenders(self):
