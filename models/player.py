from .base import Base
import random


class Player(Base):
    name = None

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
                "skillset": self.generate_random_int()
            }
            self._collection.insert_one(temp)
            self.print_dot(k)

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

    def select_random_player(self):
        count = self._collection.count()
        return dict(self._collection.find()[random.randrange(count)])
