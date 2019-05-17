from ga import Ga
from models.team import Team
import inquirer

formation_shortcuts = []
for i in Team.formations:
    formation_shortcuts.append(i[0])

questions = [
    inquirer.List('formation',
                  message="Choose prefered formation",
                  choices=formation_shortcuts,
                  ),
]
answers = inquirer.prompt(questions)
form = answers["formation"]

ga = Ga(form)
ga.run()
