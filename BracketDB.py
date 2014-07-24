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
