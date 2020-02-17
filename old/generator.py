#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
from pymongo import MongoClient
from player import Player
import os
from dotenv import find_dotenv, load_dotenv

parser = argparse.ArgumentParser(description="Football Generator")
parser.add_argument("--players", help="Create players", type=int)
parser.add_argument("--fields", help="Create fields", type=int)
args = parser.parse_args()

try:
    load_dotenv(find_dotenv())
    MONGO_IP = os.environ.get("MONGODB_IP")
    conn = MongoClient(host=[MONGO_IP])
except:
    print("Could not connect to MongoDB")

if args.players:
    player = Player(conn)
    player.remove_all_players()
    player.create(args.players)
