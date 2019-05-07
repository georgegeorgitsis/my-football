from models.player import Player
from models.team import Team
from pymongo import MongoClient

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


def nextGeneration(currentGen, eliteSize, mutationRate):
    popRanked = best_teams(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration


def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index", "Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100 * random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i, 3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults


def genetic_algorithm(individuals, eliteSize, mutationRate, generations):
    population = initial_population(individuals)

    print("Initial fitness: " + str(best_teams(population)[0].fitness))

    progress = []
    progress.append(best_teams(population)[0].fitness)
    print(best_teams(population)[0].fitness)
    # for i in range(0, generations):
    # pop = nextGeneration(population, eliteSize, mutationRate)
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


genetic_algorithm(individuals=10, eliteSize=20, mutationRate=0.01, generations=20)
