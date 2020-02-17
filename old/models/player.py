from .base import Base
from random import randint
import random


class Player(Base):
    name = None
    max_skillset = 10
    minimum_age = 18
    maximum_age = 35

    def __init__(self, conn):
        super(Player, self).__init__(conn)
        self._collection = self._db.players

    def create(self, items):
        print("Creating players...")

        for k in range(0, items):
            temp = {
                "name": self.generate_name(5),
                "surname": self.generate_name(8),
                "age": self.generate_age(),
                "position": self.generate_position()[0],
                "skillset": self.generate_random_skill(),
                "captain": self.generate_captain()
            }
            self._collection.insert_one(temp)
            self.print_dot()
        print('Complete')

    def display_all_players(self):
        print('Displaying all players...')
        cursor = self._collection.find()
        for record in cursor:
            print(record)

    def remove_all_players(self):
        print('Removing all players...')
        self._collection.delete_many({})

    def select_players(self, items):
        return self._collection.find().limit(items)

    def select_random_players(self, number=1):
        result = self._collection.aggregate([
            {"$sample": {"size": number}}
        ])

        return result.next() if number == 1 else result

    def generate_random_skill(self):
        return randint(1, self.max_skillset)

    def generate_captain(self):
        return 1 if random.random() < 0.2 else 0

    def generate_age(self):
        return randint(self.minimum_age, self.maximum_age)
