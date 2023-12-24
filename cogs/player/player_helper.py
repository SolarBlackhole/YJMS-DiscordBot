import requests
import discord
import json
import requests

from config import config as config_main

config = config_main["player"]

def setup():
    tempDict = {}

    try:
        with open(config["save_location"] + "players.json") as f:
            pass
        f.close()
    except IOError as e:
        print("player file not found... Making it now")
        f = open(config["save_location"] + "players.json", "w")
        f.write('{"players": {}}')
        f.close()

    with open(config["save_location"] + "players.json") as f:
        tempDict = json.load(f)

    f.close()

    for key in tempDict.keys():
        config[key] = tempDict[key]

def player_check(player: str):
    if player in config["players"].keys():
        return True
    else:
        return False
    
def player_add(player: str, discord_id: discord.member.Member):
    config["players"][player] = {
        "discord_account": str(discord_id),
    }
    with open(config["save_location"] + "players.json", "w") as f:
        json.dump(config["players"], f)
    f.close()

def player_remove(player: str):
    config["players"].pop(player)
    with open(config["save_location"] + "players.json", "w") as f:
        json.dump(config["players"], f)
    f.close()

def player_link(player: str, discord_id: discord.member.Member):
    config["players"][player]["discord_account"] = str(discord_id)
    with open(config["save_location"] + "players.json", "w") as f:
        json.dump(config["players"], f)
    f.close()

    

def get_info(player: str):
    information = requests.get(f"https://collegefootballrisk.com/api/player?player={player}")
    if not information:
        return None
    information = information.json()
    stars = information["ratings"]["overall"]
    totalTurns = information["ratings"]["totalTurns"]
    gameTurns = information["ratings"]["gameTurns"]
    mvps = information["ratings"]["mvps"]
    streak = information["ratings"]["streak"]
    return {
        "stars": stars,
        "totalTurns": totalTurns,
        "gameTurns": gameTurns,
        "mvps": mvps,
        "streak": streak,
    }
