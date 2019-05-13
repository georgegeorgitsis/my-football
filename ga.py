from models.player import Player
from models.team import Team
from pymongo import MongoClient
from random import randint

import random
import time
import numpy as np, operator, pandas as pd


def initial_population(individuals):
    population = []

    for i in range(0, individuals):
        team = Team(conn, player_model)
        team.create_random_team()
        team.calculate_fitness()
        population.append(team)

    return population


def calculate_fitness(population):
    for i in population:
        i.calculate_fitness()


def best_teams(population):
    return sorted(population, key=lambda team: team.fitness, reverse=True)


def next_generation(population, elite_size, mutation_rate):
    # selection_result = tournament_selection(population, elite_size)

    mating_pool = roulette_selection(population)

    # print('mating pool length is %s' % len(mating_pool))

    # matingpool = mating_pool(current_gen, selection_results)

    next_population = crossover_population(mating_pool)

    # print('next population length is %s' % len(next_population))

    # population = mutate_population(population, mutation_rate)
    return next_population


def roulette_selection(population):
    mating_pool = []

    for i in range(0, len(population)):
        selected_parent = do_roulette(population)
        # selected_parent2 = do_roulette(population)
        # children = crossover(selected_parent1, selected_parent2)
        mating_pool.append(selected_parent)

    return mating_pool


def do_roulette(population):
    max_fitness = sum(c.fitness for c in population)
    random_pick = random.uniform(0, max_fitness)

    current = 0
    for i in population:
        current += i.fitness
        if current > random_pick:
            return i


def crossover_population(population):
    next_population = []
    while population:
        parent1 = population.pop()
        parent2 = population.pop()

        children = crossover(parent1, parent2)
        next_population = next_population + children

    return next_population


def crossover(parent_team1, parent_team2):
    temp_parent_1 = parent_team1
    temp_parent_2 = parent_team2
    child_team1 = Team(conn, Player(conn))
    child_team2 = Team(conn, Player(conn))

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


def tournament_selection(population, elite_size):
    # sort teams to have the best in the beggining
    print('TOURNAMENT SELECTION FOR:')
    display_teams(population)
    print('SORT OF POPULATION FOR ELITISM:')
    population = best_teams(population)
    display_teams(population)

    selection_results = []

    for i in range(0, elite_size):
        selection_results.append(population[0])
        del population[0]
    print('START OF ELITISM ')
    display_teams(selection_results)
    print('END OF ELITISM')

    choices = {chromosome: chromosome.fitness for chromosome in population}
    # print(choices)
    exit()
    # print('START OF LOCAL TOURNAMENTS')
    # for i in range(0, len(population)):
    #     tournament = []
    #     print('TOURNAMENT ROUND %s' % i)
    #     print('SELECTING INDIVIDUALS FOR TOURNAMENT')
    #     # for k in range(0, TOURNAMENT_PLAYERS):
    #     #     tournament.append(random.choice(population))
    #     tournament = random.sample(population, TOURNAMENT_PLAYERS)
    #
    #     print('selected individuals:')
    #     display_teams(tournament)
    #     winner = best_teams(tournament)[0]
    #     print('winner is %s' % winner)
    #     selection_results.append(winner)
    #     print('SELECTION RESULTS WITH WINNER:')
    #     display_teams(selection_results)
    #
    # print('RESULTS OF TOURNAMENT')
    # display_teams(selection_results)
    # print('END OF TOURNAMENTS')

    exit()
    return selection_results


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


def mutate_population(population, mutation_rate):
    mutated_population = []

    for ind in range(0, len(population)):
        mutated = mutate(population[ind], mutation_rate)
        mutated_population.append(mutated)
    return mutated_population


def mutate(individual, mutation_rate):
    for i in range(0, len(individual.players)):
        if random.random() < mutation_rate:
            individual.players[i] = player_model.select_random_player()
    return individual


def display_teams(population):
    for i in population:
        print("Total fitness for team %s is %s" % (i, i.fitness))
    print('*** separator *** ')
    print(' ')


def genetic_algorithm(individuals, elite_size, mutation_rate, generations):
    start = time.time()
    population = initial_population(individuals)

    # print('Initial population')
    # display_teams(population)
    print("Initial best fitness: " + str(best_teams(population)[0].fitness))

    for i in range(0, generations):
        population = next_generation(population, elite_size, mutation_rate)
        iter = time.time()

        # print('Time lapsed for iteration %s is %s' % (i, iter - start))
        print("run number %s has fitness: %s " % (i, str(best_teams(population)[0].fitness)))


try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

TOURNAMENT_PLAYERS = 2
player_model = Player(conn)

genetic_algorithm(individuals=100, elite_size=2, mutation_rate=0.01, generations=500)
