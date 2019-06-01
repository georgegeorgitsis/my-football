from models.player import Player
from models.team import Team
from random import randint
import random
import matplotlib.pyplot as plt
import datetime
import time


class Ga:
    formation = None
    termination_after = -50

    def __init__(self, conn, formation_index):
        self.conn = conn
        self.formation_index = formation_index
        self.formation = Team.formations[formation_index]
        self.player_model = Player(self.conn)

    # create initial Teams with random Players
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
            mating_pool.append(self.do_roulette(temp))

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

        for i in range(0, Team.players_count):
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
        self.initial_print()

        population = self.initial_population(individuals)
        best_team = self.best_teams(population)[0]
        progress.append(best_team.fitness)
        print(' ')
        print("... Random generation best team: %s has fitness: %s " % (
            best_team.get_team_positions(), str(best_team.fitness)))

        stabilised = False
        i = 0
        while not stabilised:
            population = self.next_generation(population, elite_size, mutation_rate)
            best_team = self.best_teams(population)[0]
            print("... Generation %s, best team: %s fitness: %s " % (
                i, best_team.get_team_positions(), str(best_team.fitness)))
            progress.append(best_team.fitness)
            i += 1
            if len(set(progress[self.termination_after:])) == 1:
                stabilised = True

        self.print_results(best_team, progress)
        self.print_plt_progress(progress)

    def run(self):
        print('Starting Genetic Algorithm ...')
        return self.genetic_algorithm(individuals=800, elite_size=20, mutation_rate=1)

    @staticmethod
    def best_teams(population):
        return sorted(population, key=lambda team: team.fitness, reverse=True)

    def initial_print(self):
        print(' ')
        print('Checking against: %s ' % self.formation_index)
        print('Formation: %s ' % str(self.formation))

        for i in range(5, 0, -1):
            print(i)
            time.sleep(1)

    def print_results(self, best_team, progress):
        print(' ')
        print('Results for formation: %s' % self.formation)
        print(' ')
        print('* Best team formation: %s has fitness: %s ' % (best_team.get_team_positions(), str(best_team.fitness)))
        print(' ')
        print('Players')
        best_team.display_players()
        print(' ')
        print("Best team of all generations had fitness: %s" % max(progress))

    def print_plt_progress(self, progress):
        print(' ')
        filename = str(self.formation_index) + '_' + str(datetime.datetime.now()) + '.png'
        fig = plt.figure()
        plt.plot(progress)
        plt.title(self.formation_index)
        plt.ylabel('Fitness')
        plt.xlabel('Generations')
        fig.savefig('progress/' + filename, dpi=fig.dpi)
        print('You can check the generated %s file inside src/progress' % filename)
