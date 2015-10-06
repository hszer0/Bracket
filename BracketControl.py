from Game import Game

class BControl():

    def __init__(self, database):
        self.database = database

    def get_participants(self, match):
        l = self.database.get_participants(match)
        return [x[0] for x in l]

    def get_contenders(self, tid, match):
        l = self.database.get_contenders(tid, match)
        return [x[1] for x in l]

    def add_contender(self, tid, name):
        self.database.add_contender(tid, name)