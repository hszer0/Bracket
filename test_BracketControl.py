import unittest
from BracketDB import Database
from BracketControl import BControl


class BracketControlTests(unittest.TestCase):

    def setUp(self):
        self.db = Database("test.db")
        self.db.add_participant("Patrick")
        self.db.add_participant("Steven")
        self.db.add_participant("Simone")
        self.db.add_participant("Anke")
        self.tid = self.db.add_tournament("Unreal", "2014-01-01")
        self.db.add_contender(self.tid, "Patrick")
        self.db.add_contender(self.tid, "Steven")
        self.db.add_contender(self.tid, "Simone")
        self.db.add_contender(self.tid, "Anke")
        self.db.add_game(self.tid, 0, "Patrick", "Simone")
        self.db.add_game(self.tid, 0, "Steven", "Anke")

        self.bracketControl = BControl(self.db)

    def tearDown(self):
        self.db.c.execute("delete from participants")
        self.db.c.execute("delete from tournaments")
        self.db.c.execute("delete from contenders")
        self.db.c.execute("delete from scores")
        self.db.close_connection()

    def test_get_participants(self):
        for case in (("ne", ["Simone"]), ("ke", ['Anke']), ("qe", []),
                     ("e", ["Anke", "Simone", "Steven"])):
            with self.subTest():
                self.assertEqual(case[1], self.bracketControl.get_participants(case[0]))

    def test_get_contenders_from_tournament(self):
        for case in ((self.tid, "ne", ["Simone"]), (self.tid, "ke", ['Anke']), (self.tid, "qe", []),
                     (self.tid, "e", ["Anke", "Simone", "Steven"])):
            with self.subTest():
                self.assertEqual(case[2], self.bracketControl.get_contenders(case[0], case[1]))
