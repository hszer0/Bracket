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

    def get_scores(self, tid, name = None):
        result = []
        recordset = self.database.get_scores_from_tournament(tid)
        for record in recordset:
            if (name == None or name == record[2] or name == record[3]):
                game = Game(record[0], record[1], record[2], record[3])
                game.setScore1(record[4])
                game.setScore2(record[5])
                result.append(game)
        return result

    def add_contender(self, tid, name):
        self.database.add_contender(tid, name)

    def update_game_contenders(self, game1, game2):
        self.database.update_game(game1, game2)

    def swap_contenders(self, tid, name1, name2):
        game1 = self.get_scores(tid, name1)[0]
        game2 = self.get_scores(tid, name2)[0]

        if (game1.name1 == name1):
            game1.name1 = name2
        else:
            game1.name2 = name2

        if (game2.name1 == name2):
            game2.name1 = name1
        else:
            game2.name2 = name1

        self.update_game_contenders(self.get_scores(tid, name1)[0], game2)
        self.update_game_contenders(self.get_scores(tid, name2)[0], game1)
