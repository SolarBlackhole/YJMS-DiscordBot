import json
import discord
import requests
from config import config as config_main

config = config_main["util"]

def setup(guilds: list[discord.guild.Guild]):
    tempDict = {}

    try:
        with open(config["save_location"] + "util.json") as f:
            pass
        f.close()
    except IOError as e:
        print("Util file not found... Making it now")
        f = open(config["save_location"] + "util.json", "w")
        f.write('{"players": {}}')
        f.close()

    with open(config["save_location"] + "util.json") as f:
        tempDict = json.load(f)

    f.close()

    for key in tempDict.keys():
        config[key] = tempDict[key]


