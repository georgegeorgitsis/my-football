from .base import Base


class Team(Base):
    fitness = None
    players_count = 11

    playerModel = None

    def __init__(self, conn, player_model):
        super(Team, self).__init__(conn)
        self._collection = self._db.teams
        self.playerModel = player_model
        self.players = []

    def create(self, items):
        print("NOT Creating teams:")

    def display_all_teams(self):
        print('Displaying all players...')
        cursor = self._collection.find()
        for record in cursor:
            print(record)

    def fitness_positions_check(self):
        temp = []

        for i in self.players:
            temp.append(i['position'])

        uniqueness = len(set(temp))

        # we need to reverse it, since the more unique the better for positions
        score = 1 - self.normalize_value(uniqueness, 0, 11)
        # print("Score for {0} is {1}".format(uniqueness, score))

        return score

    def calculate_fitness(self):
        self.fitness = self.fitness_positions_check()
        return self.fitness

    def create_random_team(self):
        temp = []
        for k in range(0, self.players_count):
            temp.append(self.playerModel.select_random_player())
        self.players = temp

    def add_player(self, player):
        self.players.append(player)
