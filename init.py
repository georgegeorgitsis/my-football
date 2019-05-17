from ga import Ga
from models.team import Team
import inquirer

question_formation = [inquirer.List('formation', message="Choose formation", choices=Team.formations.keys(), ), ]
answers = inquirer.prompt(question_formation)

try:
    ga = Ga()
    ga.run(answers["formation"])
except:
    print("Could not connect to MongoDB")
    exit(0)
