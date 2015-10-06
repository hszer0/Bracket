import sqlite3


class Database():

    def __init__(self, db="bracket.db"):
        conn = sqlite3.connect(db)
        conn.isolation_level = None
        self.c = conn.cursor()
        self.c.execute("PRAGMA foreign_keys = ON;")

    def close_connection(self):
        self.c.close()

    def add_participant(self, name):
        self.c.execute("insert into participants (name) values (?)", (name,))

    def remove_participant(self, name):
        self.c.execute("delete from participants where name = (?)", (name,))

    def add_tournament(self, name, date):
        self.c.execute(
            "insert into tournaments (name, date) values (?, ?)", (name, date))
        return self.c.lastrowid

    def remove_tournament(self, tid):
        self.c.execute("delete from tournaments where id = ?", (tid,))

    def add_contender(self, tid, name):
        self.c.execute(
            "insert into contenders (tid, name) values (?, ?)", (tid, name))

    def remove_contender(self, tid, name):
        self.c.execute(
            "delete from contenders where tid = ? and name = ?", (tid, name))

    def get_contenders(self, tid, s):
        self.c.execute(
            "select tid, name from contenders where tid = ? and name like ? order by name", (tid, "%" + s + "%"))
        return self.c.fetchall()

    def add_game(self, game):
        self.c.execute("insert into scores (tid, round, name1, name2) values (?, ?, ?, ?)",
                       (game.tid, game.rnd, game.name1, game.name2))

    def remove_game(self, game):
        self.c.execute("delete from scores where tid = ? and round = ? and name1 = ? and name2 = ?",
                       (game.tid, game.rnd, game.name1, game.name2))

    def get_participants(self, s):
        self.c.execute(
            "select name from participants where name like ? order by name", ("%" + s + "%",))
        return self.c.fetchall()

    def get_all_tournaments(self, date="1900-01-01"):
        self.c.execute("select * from tournaments where date > ?", (date,))
        return self.c.fetchall()

    def get_scores_from_tournament(self, tid):
        self.c.execute(
            "select * from scores where tid = ? order by round, name1", (tid,))
        return self.c.fetchall()

    def update_score(self, game):
        self.c.execute("update scores set score1 = ?, score2 = ? where tid = ? and round = ? and name1 = ? and name2 = ?",
                       (game.score1, game.score2, game.tid, game.rnd, game.name1, game.name2))

    def update_game(self, originalGame, changedGame):
        self.c.execute("update scores set name1 = ?, name2 = ?, score1 = ?, score2 = ? where tid = ? and round = ? and name1 = ? and name2 = ?",
                       (changedGame.name1, changedGame.name2, changedGame.score1, changedGame.score2, originalGame.tid, originalGame.rnd, originalGame.name1, originalGame.name2))
