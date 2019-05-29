# My Football
---
by:
George Georgitsis (georgegeorgitsis@gmail.com)

## Getting Started

### Introduction
My Football is a command line script that quickly finds the best team out of thousands of random players, for a specific formation. 

The application was built using `python 3.6`, `mongoDB 4.0`, `docker-compose` and `Genetic Algorithms` 

### Installation
```
$ git clone git@github.com:georgegeorgitsis/my-football.git
```

#### How to run
```
$ docker-compose up -d && docker-compose exec app bash
$ cd my-football/src
$ python generator.py —player 10000
$ python init.py
```

#### Structure 
The structure of My Football is quite simple. It consists of 2 entities, a `Team` and a `Player`.
Each Player is randomly created and is having a string name, string surname, int age, string position, int skillset and a bool leader.
Each Team is created for the genetic algorithm purposes and is having a formation.

    

#####(GA)
My Football GA uses population of 800 individuals, elitism of 20 and 0.4 change of mutation.
`Individual: Team`
`Gene: Player`
- Elitism (20 individuals)
- Roulette selection
- Uniform crossover (random selection between parents)
- Mutation (0.4)
- Termination (check the last 50 best individuals if it reached the maximum fitness)

#####Fitness 
The team fitness is calculated based on 3 factors. 
- Formation 
- Summarize of skillset
- Having 1 leader in team

