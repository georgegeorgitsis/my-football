#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
from pymongo import MongoClient
from models.player import Player

parser = argparse.ArgumentParser(description="Football Generator")

parser.add_argument("--players", help="Create players", type=int)

parser.add_argument("--fields", help="Create fields", type=int)

args = parser.parse_args()

try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

if args.players:
    player = Player(conn)
    player.remove_all_players()
    player.create(args.players)
    # player.display_all_players()
