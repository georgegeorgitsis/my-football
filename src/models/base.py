# -*- coding: UTF-8 -*-
from abc import ABC, abstractmethod
from string import ascii_letters
from random import randint

import string
import random


class Base(ABC):
    _conn = None
    _db = None
    _collection = None
    _positions = ['GK', 'LB', 'CB', 'RB', 'LWB', 'RWB', 'LM', 'DM', 'CM', 'RM', 'AM', 'LW', 'RW', 'CF', 'ST']

    def __init__(self, conn=None):
        self._conn = conn
        self._db = conn.database

    @staticmethod
    def display_teams(population):
        for i in population:
            print("Total fitness for team %s is %s" % (i, i.fitness))
        print('*** separator *** ')
        print(' ')

    @staticmethod
    def normalize_value(val, min, max):
        return (val - min) / (max - min)

    @abstractmethod
    def create(self, items):
        pass

    @staticmethod
    def random_digits(digits=4):
        low = 10 ** (digits - 1)
        high = low * 9
        return random.randint(low, high)

    @staticmethod
    def random_letters(letters=10):
        return ''.join([random.choice(ascii_letters) for x in range(letters)])

    @staticmethod
    def print_dot(index, batch=10):
        if index % batch or index == 0:
            symbol = '.'
        else:
            symbol = '.'

        print(symbol, end='', flush=True)

    @staticmethod
    def generate_position():
        return random.choices(Base._positions)

    @staticmethod
    def generate_name(length=8):
        vowels = "aeiou"
        consonants = "".join(set(string.ascii_lowercase) - set(vowels))

        word = ""
        for i in range(length):
            if i % 2 == 0:
                word += random.choice(consonants)
            else:
                word += random.choice(vowels)
        return word

    @staticmethod
    def generate_age():
        return randint(18, 35)
