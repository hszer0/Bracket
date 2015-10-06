class Game():
    def __init__(self, tid, rnd, name1, name2):
        self.tid = tid
        self.rnd = rnd
        self.name1 = name1
        self.name2 = name2
        self.score1 = 0
        self.score2 = 0

    def setScore1(self, score):
        self.score1 = score

    def setScore2(self, score):
        self.score2 = score