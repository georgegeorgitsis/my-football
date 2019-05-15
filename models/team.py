from .base import Base
from collections import Counter


class Team(Base):
    fitness = None
    players_count = 11
    playerModel = None

    tactics = [
        ['GK', 'LB', 'CB', 'CB', 'RB', 'LM', 'CM', 'CM', 'RM', 'ST', 'ST'],  # 4-4-2
        ['GK', 'LB', 'CB', 'CB', 'RB', 'DM', 'CM', 'CM', 'LW', 'RW', 'ST'],  # 4-3-3
        ['GK', 'CB', 'CB', 'CB', 'RWB', 'LWB', 'CM', 'CM', 'CM', 'ST', 'ST'],  # 5-3-2
    ]

    def __init__(self, conn, player_model, tactic):
        super(Team, self).__init__(conn)
        self._collection = self._db.teams
        self.playerModel = player_model
        self.players = []
        self.tactic = tactic

    def create(self, items):
        print("NOT Creating teams:")

    def display_all_teams(self):
        print('Displaying all players...')
        cursor = self._collection.find()
        for record in cursor:
            print(record)

    def fitness_positions_uniq_check(self):
        temp = []
        for i in self.players:
            temp.append(i['position'])

        uniqueness = len(set(temp))
        score = self.normalize_value(uniqueness, 0, 11)
        result = sorted(temp, key=lambda x: Base._positions.index(x) if x in Base._positions else len(Base._positions))
        print('Team: %s has uniqueness: %s and score: %s' % (str(result), uniqueness, score))
        return score

    def fitness_against_tactic(self):
        temp = []
        for i in self.players:
            temp.append(i['position'])

        diff = sum((Counter(self.tactic) - Counter(temp)).values())
        score = 11 - diff

        return score

    def calculate_fitness(self):
        self.fitness = self.fitness_against_tactic()
        return self.fitness

    def get_team_positions(self):
        temp = []
        for i in self.players:
            temp.append(i['position'])

        result = sorted(temp, key=lambda x: Base._positions.index(x) if x in Base._positions else len(Base._positions))

        return result

    def add_player(self, player):
        self.players.append(player)
