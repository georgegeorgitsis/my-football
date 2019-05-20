from ga import Ga
from models.team import Team
import inquirer
from pymongo import MongoClient
from pymongo import errors as mongoerrors


question_formation = [inquirer.List('formation', message="Choose formation", choices=Team.formations.keys(), ), ]
answers = inquirer.prompt(question_formation)

conn = MongoClient('152.23.0.2')

try:
    ga = Ga(conn, answers["formation"])
    ga.run()
except:
    print('exception')
