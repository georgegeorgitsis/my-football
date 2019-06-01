# My Football
---
by:
George Georgitsis (georgegeorgitsis@gmail.com)

## Getting Started

### Introduction
My Football is a command line script that quickly finds the best team out of thousands of random players, for a specific formation. 

The application was built using `python 3.6`, `mongoDB 4.0`, `docker-compose` and `Genetic Algorithms` 


### Installation - How to run
```
$ git clone https://github.com/georgegeorgitsis/my-football
$ cd my-football
Copy .env.example to .env
$ docker-compose up -d && docker-compose exec app bash
$ cd my-football/src
$ python generator.py --players 10000
$ python init.py
```

### Structure 
The structure of My Football is quite simple. It consists of 2 entities, a `Team` and a `Player`.
Each Player is randomly created and is having a string name, string surname, int age, string position, int skillset and a flag captain.
Each Team is created for the genetic algorithm purposes and is having a formation.

### Generator
The generator.py simply creates the given amount of players with random attributes in the database. 
In the `Installation - How to run` section, the example code creates 10000, while they could be more but not lower than 8800,
since we use populations of 800 teams, multiplied by 11 players for each team. 

The different combinations of finding the best r(11) players for team out of n(10000) players is produced via the formula 
`C(n,r) = n!/(r!(n−r)!)`. That said, the different combinations are more than `2370686044157731915491600000`   
---
### Player 

#### Name/surname
Names, surnames, characteristics etc. of players are randomly created. Any resemblance to actual players or positions or formations, is entirely coincidental.  

#### Positions
Each player has a specific position in the field and it is randomly assigned to him via the generator.py
`'GK', 'LB', 'CB', 'RB', 'LWB', 'RWB', 'LM', 'DM', 'CM', 'RM', 'AM', 'LW', 'RW', 'CF', 'ST'`

#### Age / Skillset
Age and skillset is also randomly assigned to a player via the generator.py.
Skillset is a random number between 1 and 10, while 10 is the maximum. 
Age is also randomly selected between 18 and 35.

#### Captain
Captainship is assigned to players with a chance of 0.2. Captain value 1 means that the player 
is having a captain role in the team.
---
### Team 
A team has always 11 players and a specific selected formation

#### Formations
```
4-4-2: [GK, LB, CB, CB, RB, LM, CM, CM, RM, ST, ST]
4-4-1-1: [GK, LB, CB, CB, RB, LM, CM, CM, RM, AM, ST]
4-2-3-1: [GK, LB, CB, CB, RB, DM, DM, AM, LW, RW, ST]
4-2-2-2: [GK, LWB, CB, CB, RWB, DM, DM, AM, AM, ST, ST]
4-1-2-3: [GK, LB, CB, CB, RB, DM, CM, CM, LW, RW, ST]
4-3-3: [GK, LB, CB, CB, RB, CM, CM, CM, LW, RW, ST]
4-3-2-1: [GK, LB, CB, CB, RB, CM, CM, CM, AM, AM, ST]
5-1-2-2: [GK, LWB, CB, CB, CB, RWB, DM, CM, CM, ST, ST]
5-1-3-1: [GK, LWB, CB, CB, CB, RWB, DM, LM, CM, RM, ST]
5-3-2: [GK, LWB, CB, CB, CB, RWB, CM, CM, CM, ST, ST]
5-4-1: [GK, LWB, CB, CB, CB, RWB, LM, CM, CM, RM, ST]
3-4-3: [GK, CB, CB, CB, LM, CM, CM, RM, LW, RW, ST]
3-5-2: [GK, CB, CB, CB, DM, DM, LM, RM, AM, ST, ST]
3-6-1: [GK, CB, CB, CB, DM, DM, LM, RM, AM, AM, ST]
```

#### Fitness / Score of team
A team is evaluated for it's score based on the following criteria:
- The number of matching positions of the players compared to the selected formation for the team
- The sum of the skillset of the players in the team
- The number of captains in the team. Best scenario is having 1 captain in the team.
- The age of the players. The younger the team the better.

---
### (GA)
My Football GA uses population of 800 individuals, elitism of 20 and 1 chance of mutation.

- Elitism (20 individuals)
- Roulette selection
- Uniform crossover (random selection between parents)
- Mutation (1)
- Termination (last 50 best individuals is not changing fitness)

After every run of the GA, you can find the progress graph as a png inside `src/progress/temp.png` which overrides the previous one.