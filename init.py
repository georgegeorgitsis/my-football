from ga import Ga
from models.team import Team
import inquirer

formation_shortcuts = []
for i in Team.formations:
    formation_shortcuts.append(i)

questions = [
    inquirer.List('formation',
                  message="Choose prefered formation",
                  choices=formation_shortcuts,
                  ),
]
answers = inquirer.prompt(questions)

try:
    ga = Ga(answers["formation"])
    ga.run()
except:
    print("Could not connect to MongoDB")
    exit(0)
