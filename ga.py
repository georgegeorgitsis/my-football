from models.player import Player
from models.team import Team
from pymongo import MongoClient
from random import randint

import random
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
    selection_result = selection(population, elite_size)

    # matingpool = mating_pool(current_gen, selection_results)

    next_population = crossover_population(selection_result, elite_size)

    # population = mutate_population(population, mutation_rate)
    return next_population


def selection(population, elite_size):
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
    print(weighted_random_choice(choices))
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


def weighted_random_choice(choices):
    max = sum(choices.values())
    pick = random.uniform(0, max)
    current = 0
    for key, value in choices.items():
        current += value
        if current > pick:
            return key


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
        print("Total fitness for team %s is %s" % (i, i.fitness))
    print('*** separator *** ')
    print(' ')


def genetic_algorithm(individuals, elite_size, mutation_rate, generations):
    population = initial_population(individuals)

    print('Initial population')
    display_teams(population)
    print("Initial best fitness: " + str(best_teams(population)[0].fitness))

    for i in range(0, generations):
        population = next_generation(population, elite_size, mutation_rate)

        calculate_fitness(population)
        display_teams(population)
        exit()
        print("fitness: " + str(best_teams(population)[0].fitness))


try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

TOURNAMENT_PLAYERS = 2
player_model = Player(conn)

genetic_algorithm(individuals=6, elite_size=2, mutation_rate=0.01, generations=5)
