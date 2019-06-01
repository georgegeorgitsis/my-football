from ga import Ga
from models.team import Team
from pymongo import MongoClient
from dotenv import find_dotenv, load_dotenv
import inquirer
import os

question_formation = [inquirer.List('formation', message="Choose formation", choices=Team.formations.keys(), ), ]
answers = inquirer.prompt(question_formation)

try:
    load_dotenv(find_dotenv())
    MONGO_IP = os.environ.get("MONGODB_IP")
    conn = MongoClient(host=[MONGO_IP])

    ga = Ga(conn, answers["formation"])
    ga.run()
except Exception as ex:
    print('exception')
