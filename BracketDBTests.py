import unittest
from BracketDB import Database


class BracketDBTests(unittest.TestCase):

    def setUp(self):
        self.db = Database("test.db")

    def tearDown(self):
        self.db.c.execute("delete from participants")
        self.db.c.execute("delete from tournaments")
        self.db.c.execute("delete from contenders")
        self.db.c.execute("delete from scores")
        self.db.close_connection()

    def test_tables_and_columns(self):
        """Tables contain all required columns"""
        self.db.c.execute("select name from participants")
        self.db.c.execute("select id, name, date from tournaments")
        self.db.c.execute("select tid, name from contenders")
        self.db.c.execute(
            "select tid, round, name1, name2, score1, score2 from scores")

    def test_add_and_remove_participant(self):
        """Participant can be added and removed"""
        # first clear the table
        self.db.c.execute("delete from participants")

        # test for adding
        self.db.add_participant("Patrick")
        self.db.c.execute("select name from participants")
        row = self.db.c.fetchone()
        self.assertEqual("Patrick", row[0])

        # test for removing
        self.db.remove_participant("Patrick")
        self.db.c.execute("select name from participants")
        self.assertIsNone(self.db.c.fetchone())

    def test_add_and_remove_tournament(self):
        """Tournament can be added and removed"""

        # test for adding
        tid = self.db.add_tournament("UT2k4", "2014-01-01")
        self.db.c.execute("select name, date from tournaments")
        row = self.db.c.fetchone()
        self.assertEqual(("UT2k4", "2014-01-01"), row)

        # test for removing
        self.db.remove_tournament(tid)
        self.db.c.execute("select id from tournaments")
        self.assertIsNone(self.db.c.fetchone())

    def test_add_and_remove_contender(self):
        """Contender can be added and removed"""

        # test for adding
        tid = self.db.add_tournament("UT2k4", "2014-01-01")
        self.db.add_contender(tid, "Patrick")
        self.db.c.execute("select tid, name from contenders")
        row = self.db.c.fetchone()
        self.assertEqual((tid, "Patrick"), row)

        # test for removing
        self.db.remove_contender(tid, "Patrick")
        self.db.remove_tournament(tid)
        self.db.c.execute("select * from contenders")
        self.assertIsNone(self.db.c.fetchone())

    def test_add_and_remove_game(self):
        """Game can be added and removed"""

        # test for adding
        tid = self.db.add_tournament("UT2k4", "2014-01-01")
        self.db.add_game(tid, 1, "Patrick", "Steven")

        # test for removing
        self.db.remove_game(tid, 1, "Patrick", "Steven")
        self.db.remove_tournament(tid)
        self.db.c.execute("select * from scores")
        self.assertIsNone(self.db.c.fetchone())

    def test_get_participants_containing_letter(self):
        """Retrieve participants containing a letter"""
        self.db.add_participant("Patrick")
        self.db.add_participant("Steven")
        self.db.add_participant("Simone")
        self.db.add_participant("Anke")

        self.assertEqual(
            [("Anke",), ("Simone",), ("Steven",)], self.db.get_participants("e"))
        for case in (("e", [("Anke",), ("Simone",), ("Steven",)]), ("t", [('Patrick',), ('Steven',)]), ("q", [])):
            with self.subTest():
                self.assertEqual(case[1], self.db.get_participants(case[0]))

    def test_get_participants_containing_string(self):
        """Retrieve participants containing a string"""
        self.db.add_participant("Patrick")
        self.db.add_participant("Steven")
        self.db.add_participant("Simone")
        self.db.add_participant("Anke")

        self.assertEqual(
            [("Anke",), ("Simone",), ("Steven",)], self.db.get_participants("e"))
        for case in (("ne", [("Simone",)]), ("ke", [('Anke',)]), ("qe", [])):
            with self.subTest():
                self.assertEqual(case[1], self.db.get_participants(case[0]))

    def test_get_all_tournaments(self):
        """Retrieve all tournaments"""
        id1 = self.db.add_tournament("UT2k4", "2014-01-01")
        id2 = self.db.add_tournament("Worms", "2013-01-01")
        self.assertEqual(self.db.get_all_tournaments(), [
                         (id1, 'UT2k4', '2014-01-01'), (id2, 'Worms', '2013-01-01')])

    def test_get_all_tournaments_from_date(self):
        """Retrieve all tournaments from certain date"""
        id1 = self.db.add_tournament("UT2k4", "2014-01-01")
        self.db.add_tournament("Worms", "2013-01-01")
        self.assertEqual(
            self.db.get_all_tournaments("2013-05-09"), [(id1, 'UT2k4', '2014-01-01')])

    def test_get_all_scores_from_tournament(self):
        """Retrieve all scores from tournament"""
        tid = self.db.add_tournament("UT2k4", "2014-01-01")
        self.db.add_game(tid, 0, "Patrick", "Steven")
        self.db.add_game(tid, 0, "Anke", "Simone")
        self.db.add_game(tid, 1, "Steven", "Anke")
        self.assertEqual(self.db.get_scores_from_tournament(tid),
                         [(tid, 0, 'Anke', 'Simone', 0, 0), (tid, 0, 'Patrick', 'Steven', 0, 0),
                          (tid, 1, 'Steven', 'Anke', 0, 0)])

    def test_update_score(self):
        """Update score"""
        self.db.add_game(1, 0, "Patrick", "Steven")
        self.db.update_score(1, 0, "Patrick", "Steven", 1, 2)
        self.db.c.execute(
            "select * from scores where tid = 1 and round = 0 and name1 = 'Patrick' and name2 = 'Steven'")
        row = self.db.c.fetchone()
        self.assertEqual(row[4], 1)
        self.assertEqual(row[5], 2)

# TODO: Swap contenders
# TODO: Generate round 1
# TODO: Generate next round
