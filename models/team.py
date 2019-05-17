from .base import Base
from collections import Counter


class Team(Base):
    fitness = None
    players_count = 11
    playerModel = None

    tactics = [
        ['GK', 'LB', 'CB', 'CB', 'RB', 'LM', 'CM', 'CM', 'RM', 'ST', 'ST'],  # 4-4-2
        ['GK', 'LB', 'CB', 'CB', 'RB', 'LM', 'CM', 'CM', 'RM', 'AM', 'ST'],  # 4-4-1-1
        ['GK', 'LB', 'CB', 'CB', 'RB', 'CM', 'CM', 'CM', 'LW', 'RW', 'ST'],  # 4-4-1-1
        ['GK', 'LB', 'CB', 'CB', 'RB', 'DM', 'DM', 'AM', 'LW', 'RW', 'ST'],  # 4-2-3-1
        ['GK', 'LWB', 'CB', 'CB', 'RWB', 'DM', 'DM', 'AM', 'AM', 'ST', 'ST'],  # 4-2-2-2
        ['GK', 'LB', 'CB', 'CB', 'RB', 'DM', 'CM', 'CM', 'LW', 'RW', 'ST'],  # 4-1-2-3
        ['GK', 'LB', 'CB', 'CB', 'RB', 'CM', 'CM', 'CM', 'LW', 'RW', 'ST'],  # 4-3-3
        ['GK', 'LB', 'CB', 'CB', 'RB', 'CM', 'CM', 'CM', 'AM', 'AM', 'ST'],  # 4-3-2-1
        ['GK', 'LWB', 'CB', 'CB', 'CB', 'RWB', 'DM', 'CM', 'CM', 'ST', 'ST'],  # 5-1-2-2
        ['GK', 'LWB', 'CB', 'CB', 'CB', 'RWB', 'DM', 'LM', 'CM', 'RM', 'ST'],  # 5-1-3-1
        ['GK', 'LWB', 'CB', 'CB', 'CB', 'RWB', 'CM', 'CM', 'CM', 'ST', 'ST'],  # 5-3-2
        ['GK', 'LWB', 'CB', 'CB', 'CB', 'RWB', 'LM', 'CM', 'CM', 'RM', 'ST'],  # 5-4-1
        ['GK', 'CB', 'CB', 'CB', 'LM', 'CM', 'CM', 'RM', 'LW', 'RW', 'ST'],  # 3-4-3
        ['GK', 'CB', 'CB', 'CB', 'DM', 'DM', 'LM', 'RM', 'AM', 'ST', 'ST'],  # 3-5-2
        ['GK', 'CB', 'CB', 'CB', 'DM', 'DM', 'LM', 'RM', 'AM', 'AM', 'ST'],  # 3-6-1
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

    # def fitness_positions_uniq_check(self):
    #     temp = []
    #     for i in self.players:
    #         temp.append(i['position'])
    #
    #     uniqueness = len(set(temp))
    #     score = self.normalize_value(uniqueness, 0, 11)
    #     result = sorted(temp, key=lambda x: Base._positions.index(x) if x in Base._positions else len(Base._positions))
    #     print('Team: %s has uniqueness: %s and score: %s' % (str(result), uniqueness, score))
    #     return score

    def fitness_against_tactic(self):
        temp_positions = []
        for i in self.players:
            temp_positions.append(i['position'])

        diff = sum((Counter(self.tactic) - Counter(temp_positions)).values())
        tactic_score = Team.players_count - diff
        return self.normalize_value(tactic_score, 0, Team.players_count)

    def fitness_against_skillset(self):
        skillset_score = 0

        for i in self.players:
            skillset_score += i['skillset']

        return self.normalize_value(skillset_score, 0, Team.players_count * self.playerModel.max_skillset)

    def fitness_against_leadership(self):
        leader_sum = 0

        for i in self.players:
            leader_sum += i['leader']

        leadership_score = 4 if leader_sum == 0 else Team.players_count - leader_sum

        # we need at least one leader in a team
        return self.normalize_value(leadership_score, 0, Team.players_count)

    def calculate_fitness(self):
        self.fitness = self.fitness_against_tactic() + self.fitness_against_skillset() + self.fitness_against_leadership()

        self.fitness = self.fitness * 1000
        return self.fitness

    def get_team_positions(self):
        temp = []
        for i in self.players:
            temp.append(i['position'])

        result = sorted(temp, key=lambda x: Base._positions.index(x) if x in Base._positions else len(Base._positions))

        return result

    def add_player(self, player):
        self.players.append(player)

    def display_players(self):
        for i in self.players:
            print(i)
