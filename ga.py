from models.player import Player
from models.team import Team
from pymongo import MongoClient
import numpy as np, random, operator, pandas as pd

try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

player_model = Player(conn)


# players = player_model.select_random_player()


def initial_population(individuals):
    population = []

    for i in range(0, individuals):
        team = Team(conn, player_model)
        team.create_random_team()
        team.calculate_fitness()
        population.append(team)

    return population


def best_teams(population):
    return sorted(population, key=lambda team: team.fitness, reverse=True)


def next_generation(current_gen, elite_size, mutation_rate):
    pop_ranked = best_teams(current_gen)
    selection_results = tournament_selection(pop_ranked, elite_size)
    matingpool = mating_pool(current_gen, selection_results)
    children = breed_population(matingpool, elite_size)
    # nextGeneration = mutatePopulation(children, mutation_rate)
    # return nextGeneration


def tournament_selection(pop_ranked, elite_size):
    selection_results = []

    for i in range(0, elite_size):
        selection_results.append(pop_ranked[0])
    for i in range(0, len(pop_ranked) - elite_size):
        tournament = []
        for k in range(0, 3):
            tournament.append(random.choice(pop_ranked))

        selection_results.append(best_teams(tournament)[0])

    return selection_results


def mating_pool(population, selection_results):
    mating_pool_list = []
    for i in range(0, len(selection_results)):
        index = selection_results[i]
        mating_pool_list.append(population[index])
    return mating_pool_list


def breed_population(matingpool, elite_size):
    children = []
    length = len(matingpool) - elite_size
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0, elite_size):
        children.append(matingpool[i])

    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool) - i - 1])
        children.append(child)
    return children


def breed(parent1, parent2):
    child = []
    child1 = []
    child2 = []

    gene_1 = int(random.random() * len(parent1))
    gene_2 = int(random.random() * len(parent1))

    start_gene = min(gene_1, gene_2)
    end_gene = max(gene_1, gene_2)

    for i in range(start_gene, end_gene):
        child1.append(parent1[i])

    child2 = [item for item in parent2 if item not in child1]

    child = child1 + child2
    return child


def genetic_algorithm(individuals, elite_size, mutation_rate, generations):
    population = initial_population(individuals)

    print("Initial fitness: " + str(best_teams(population)[0].fitness))

    progress = []
    progress.append(best_teams(population)[0].fitness)
    # print(best_teams(population)[0].fitness)
    for i in range(0, generations):
        pop = next_generation(population, elite_size, mutation_rate)


#     # print("Generation: " + str(i) + " - distance: " + str(1 / rankRoutes(pop)[0][1]))
#     # print("distance: " + str(1 / rankRoutes(pop)[0][1]))
#     progress.append(1 / rankRoutes(pop)[0][1])
#     last_n = progress[-15:]
#     print(last_n.count(last_n[-1]))
#     # print('[%s]' % ', '.join(map(str, progress[-10:])))
#
# print("Final distance: " + str(1 / rankRoutes(pop)[0][1]))
# bestRouteIndex = rankRoutes(pop)[0][0]
# bestRoute = pop[bestRouteIndex]
# return bestRoute


genetic_algorithm(individuals=20, elite_size=10, mutation_rate=0.01, generations=20)
