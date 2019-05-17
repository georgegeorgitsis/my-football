from models.player import Player
from models.team import Team
from pymongo import MongoClient
from random import randint
import matplotlib.pyplot as plt
import random


class Ga:

    def __init__(self, selected_formation_index):

        self.conn = MongoClient()
        self.selected_formation_index = selected_formation_index
        self.formation = Team.formations[selected_formation_index]
        self.player_model = Player(self.conn)

    def initial_population(self, individuals):
        population = []

        number_of_random_players = individuals * Team.players_count
        random_players = self.player_model.select_random_players(number_of_random_players)

        for i in range(0, individuals):
            team = Team(self.conn, self.player_model, self.formation)
            for k in range(0, Team.players_count):
                team.add_player(random_players.next())
            team.calculate_fitness()
            population.append(team)

        return population

    @staticmethod
    def best_teams(population):
        return sorted(population, key=lambda team: team.fitness, reverse=True)

    def next_generation(self, population, elite_size, mutation_rate):
        mating_pool = self.roulette_selection(population, elite_size)

        random.shuffle(mating_pool)

        crossovered = self.crossover_population(mating_pool)

        population = self.mutate_population(crossovered, mutation_rate)

        return population

    def roulette_selection(self, population, elite_size):
        temp = population
        population = self.best_teams(population)
        mating_pool = population[:elite_size]
        del temp[:elite_size]

        for i in range(0, len(population) - elite_size):
            selected_parent = self.do_roulette(temp)
            mating_pool.append(selected_parent)

        return mating_pool

    def do_roulette(self, population):
        max_fitness = sum(c.fitness for c in population)
        random_pick = random.uniform(0, max_fitness)

        current = 0
        for i in population:
            current += i.fitness
            if current > random_pick:
                return i

    def crossover_population(self, population):
        next_population = []
        while population:
            parent1 = population.pop()
            parent2 = population.pop()

            children = self.crossover(parent1, parent2)
            next_population = next_population + children

        return next_population

    def crossover(self, parent_team1, parent_team2):
        temp_parent_1 = parent_team1
        temp_parent_2 = parent_team2
        child_team1 = Team(self.conn, Player(self.conn), self.formation)
        child_team2 = Team(self.conn, Player(self.conn), self.formation)

        for i in range(0, 11):
            if randint(0, 1) == 1:
                random_player1 = temp_parent_1.players[i]
                random_player2 = temp_parent_2.players[i]
            else:
                random_player1 = temp_parent_2.players[i]
                random_player2 = temp_parent_1.players[i]

            child_team1.players.append(random_player1)
            child_team2.players.append(random_player2)

        child_team1.calculate_fitness()
        child_team2.calculate_fitness()

        return [child_team1, child_team2]

    def mutate_population(self, population, mutation_rate):
        if random.random() < mutation_rate:
            random_index = random.randint(0, len(population) - 1)
            population[random_index] = self.mutate(population[random_index])
        return population

    def mutate(self, individual):
        random_team_player = randint(0, Team.players_count - 1)
        del individual.players[random_team_player]
        individual.players.append(self.player_model.select_random_players())
        individual.calculate_fitness()

        return individual

    def genetic_algorithm(self, individuals, elite_size, mutation_rate):
        progress = []

        print('Checking against: %s' % str(self.formation))
        population = self.initial_population(individuals)
        best_team = self.best_teams(population)[0]
        progress.append(best_team.fitness)
        print(" ... Random generation best team: %s has fitness: %s " % (
            best_team.get_team_positions(), str(best_team.fitness)))

        stabilised = False
        i = 0
        while not stabilised:
            population = self.next_generation(population, elite_size, mutation_rate)
            best_team = self.best_teams(population)[0]
            print(" ... Generation number %s, best team: %s has fitness: %s " % (
                i, best_team.get_team_positions(), str(best_team.fitness)))
            progress.append(best_team.fitness)
            i += 1
            if len(set(progress[-50:])) == 1:
                stabilised = True

        print(' ')
        print(" Final result: best team: %s has fitness: %s " % (
            best_team.get_team_positions(), str(best_team.fitness)))
        print(best_team.get_team_positions())
        print("Best team of all generations had fitness: %s" % max(progress))
        best_team.display_players()

        plt.plot(progress)
        plt.ylabel('Fitness')
        plt.xlabel('Generations')
        # plt.show()

    def run(self):
        self.genetic_algorithm(individuals=800, elite_size=20, mutation_rate=1)

# TOURNAMENT_PLAYERS = 2
#
# def tournament_selection(population, elite_size):
#     # sort teams to have the best in the beggining
#     print('TOURNAMENT SELECTION FOR:')
#     display_teams(population)
#     print('SORT OF POPULATION FOR ELITISM:')
#     population = best_teams(population)
#     display_teams(population)
#
#     selection_results = []
#
#     for i in range(0, elite_size):
#         selection_results.append(population[0])
#         del population[0]
#     print('START OF ELITISM ')
#     display_teams(selection_results)
#     print('END OF ELITISM')
#
#     choices = {chromosome: chromosome.fitness for chromosome in population}
#     print(choices)
#     exit()
#     print('START OF LOCAL TOURNAMENTS')
#     for i in range(0, len(population)):
#         tournament = []
#         print('TOURNAMENT ROUND %s' % i)
#         print('SELECTING INDIVIDUALS FOR TOURNAMENT')
#         # for k in range(0, TOURNAMENT_PLAYERS):
#         #     tournament.append(random.choice(population))
#         tournament = random.sample(population, TOURNAMENT_PLAYERS)
#
#         print('selected individuals:')
#         display_teams(tournament)
#         winner = best_teams(tournament)[0]
#         print('winner is %s' % winner)
#         selection_results.append(winner)
#         print('SELECTION RESULTS WITH WINNER:')
#         display_teams(selection_results)
#
#     print('RESULTS OF TOURNAMENT')
#     display_teams(selection_results)
#     print('END OF TOURNAMENTS')
#
#     exit()
#     return selection_results
# def crossover_population(population, elite_size):
#     next_population = []
#     length = len(population) - elite_size
#
#     pass the elitism individuals to next generation no matter what. Those individuals will
#     be the first on the list
#     for i in range(0, elite_size):
#         next_population.append(population[i])
#
#     remove them from pool, we do want to crossover with them any more
#     del population[:elite_size]
#
#     print(length)
#
#     for i in range(0, len(population), 2):
#         parent1 = population[i]
#         parent2 = population[i + 1]
#
#         child_team = crossover(parent1, parent2)
#         next_population.append(child_team)
#         child_team = crossover(parent1, parent2)
#         next_population.append(child_team)
#
#     return next_population
