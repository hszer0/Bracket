__author__ = 'Patrick.Liem'

import sqlite3, shutil, configparser


class Database(object):

    def __init__(self):
        conn = sqlite3.connect("bracket.db")
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
        self.c.execute("insert into tournaments (name, date) values (?, ?)", (name, date))
        return self.c.lastrowid

    def remove_tournament(self, tid):
        self.c.execute("delete from tournaments where id = ?", (tid,))

    def add_contender(self, tid, name):
        self.c.execute("insert into contenders (tid, name) values (?, ?)", (tid, name))

    def remove_contender(self, tid, name):
        self.c.execute("delete from contenders where tid = ? and name = ?", (tid, name))