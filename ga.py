from models.player import Player
from models.team import Team
from pymongo import MongoClient
from random import randint

import numpy as np, random, operator, pandas as pd

try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

TOURNAMENT_PLAYERS = 2
player_model = Player(conn)


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
    # population = best_teams(population)

    selection = tournament_selection(population, elite_size)

    # matingpool = mating_pool(current_gen, selection_results)

    next_population = crossover_population(selection, elite_size)

    # population = mutate_population(population, mutation_rate)
    return next_population


def tournament_selection(pop_ranked, elite_size):
    selection_results = []

    for i in range(0, elite_size):
        selection_results.append(pop_ranked[0])
    for i in range(0, len(pop_ranked) - elite_size):
        tournament = []
        for k in range(0, TOURNAMENT_PLAYERS):
            tournament.append(random.choice(pop_ranked))

        selection_results.append(best_teams(tournament)[0])

    return selection_results


# def mating_pool(population, selection_results):
#     mating_pool_list = []
#     for i in range(0, len(selection_results)):
#         index = selection_results[i]
#         mating_pool_list.append(population[index])
#
#     print(mating_pool_list)
#     exit()
#     return mating_pool_list


def crossover_population(population, elite_size):
    next_population = []
    # length = len(population) - elite_size

    # pass the elitism individuals to next generation no matter what. Those individuals will
    # be the first on the list
    # for i in range(0, elite_size):
    #     next_population.append(population[i])

    # remove them from pool, we do want to crossover with them any more
    # del population[:elite_size]

    # print(length)

    for i in range(0, len(population), 2):
        parent1 = population[i]
        parent2 = population[i + 1]

        child_team = crossover(parent1, parent2)
        next_population.append(child_team)
        child_team = crossover(parent1, parent2)
        next_population.append(child_team)

    return next_population


def crossover(parent_team1, parent_team2):
    temp_parent_1 = parent_team1
    temp_parent_2 = parent_team2
    child_team = Team(conn, Player(conn))

    for i in range(0, 11):
        if randint(0, 1) == 1:
            child_team.players.append(temp_parent_1.players[i])
        else:
            child_team.players.append(temp_parent_2.players[i])

    return child_team


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
        print("Total score for %s is %s" % (i, i.fitness))


def genetic_algorithm(individuals, elite_size, mutation_rate, generations):
    population = initial_population(individuals)

    # display_teams(population)

    print("Initial fitness: " + str(best_teams(population)[0].fitness))

    progress = []
    progress.append(best_teams(population)[0].fitness)
    # print(best_teams(population)[0].fitness)
    for i in range(0, generations):
        display_teams(population)
        population = next_generation(population, elite_size, mutation_rate)

        calculate_fitness(population)
        display_teams(population)
        exit()
        print("fitness: " + str(best_teams(population)[0].fitness))
        progress.append(best_teams(population)[0].fitness)


#     last_n = progress[-15:]
#     print(last_n.count(last_n[-1]))
#     # print('[%s]' % ', '.join(map(str, progress[-10:])))
#
# print("Final distance: " + str(1 / rankRoutes(pop)[0][1]))
# bestRouteIndex = rankRoutes(pop)[0][0]
# bestRoute = pop[bestRouteIndex]
# return bestRoute


genetic_algorithm(individuals=10, elite_size=4, mutation_rate=0.01, generations=5)
