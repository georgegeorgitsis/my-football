from ga import Ga
from models.team import Team
import inquirer
from pymongo import MongoClient

question_formation = [inquirer.List('formation', message="Choose formation", choices=Team.formations.keys(), ), ]
answers = inquirer.prompt(question_formation)

conn = MongoClient(host=['152.23.0.2'])
print('wtf')
try:
    ga = Ga(conn, answers["formation"])
    ga.run()
except Exception as ex:
    print(ex)
    print('exception')
