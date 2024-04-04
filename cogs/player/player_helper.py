import datetime
import requests
import discord
import json
import requests

from config import config as config_main

config = config_main["player"]
players = {}

def setup():
    global players
    #tempDict = {}

    try:
        with open(config["save_location"] + "players.json") as f:
            pass
        f.close()
    except IOError as e:
        print("player file not found... Making it now")
        f = open(config["save_location"] + "players.json", "w")
        f.write('{}')
        f.close()

    with open(config["save_location"] + "players.json") as f:
        players = json.load(f)

    save()
    f.close()

    
    ##for key in tempDict.keys():
    ##    config[key] = tempDict[key]
    

def save():
    global players
    with open(config["save_location"] + "players.json", "w") as f:
        json.dump(players, f)
    f.close()

def player_check(player: str):
    global players
    print(f"Players: {players}")
    if player in players:
        print("Player in players")
        return True
    print("Player not in players")
    return False
    
def player_add(player: str, discord_id: discord.member.Member):
    global players
    info = get_info(player)
    if info is None:
        return False
    players[player] = {
        "discord_account": str(discord_id),
        "platform": info["platform"],
        "stars": info["stars"],
    }
    save()

def player_remove(player: str):
    global players
    if player not in players:
        return False
    del players[player]
    save()
    return True

def player_link(player: str, discord_id: discord.member.Member):
    global players
    if player not in players:
        return False
    players[player]["discord_account"] = str(discord_id)
    save()
    return True

    

def get_info(player: str):
    information = requests.get(f"https://collegefootballrisk.com/api/player?player={player}")
    print(f"Information {information}")
    if not information:
        return None
    information = information.json()
    stars = information["ratings"]["overall"]
    totalTurns = information["ratings"]["totalTurns"]
    gameTurns = information["ratings"]["gameTurns"]
    mvps = information["ratings"]["mvps"]
    streak = information["ratings"]["streak"]
    platform = information["platform"]
    if player_check(player):
        return {
            "stars": stars,
            "totalTurns": totalTurns,
            "gameTurns": gameTurns,
            "mvps": mvps,
            "streak": streak,
            "platform": platform,
            "discord_account": players[player]["discord_account"],
        }
    return {
        "stars": stars,
        "totalTurns": totalTurns,
        "gameTurns": gameTurns,
        "mvps": mvps,
        "streak": streak,
        "platform": platform,
        "discord_account": "None Linked",
    }

def search_player(player: str):
    possible_players = requests.get(f"https://collegefootballrisk.com/api/players/search?s={player}&limit=1")
    if not possible_players:
        return None
    possible_players = possible_players.json()
    if not possible_players:
        return None
    return possible_players[0]

def api_check():
    information = requests.get(f"https://collegefootballrisk.com/api/player?player=SolarBlackhole")
    print(f"Information {information}")
    if not information:
        return False
    return True

def player_not_found():
    if api_check():
        embed = discord.Embed(
            title="Player not found",
            description="Please check the player name and try again.",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now(),
        )
        return embed
    else:
        embed = discord.Embed(
            title="API Error",
            description="The API is currently down. Please try again later.",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now(),
        )
        return embed

def is_linked(player: str):
    global players
    if player not in players:
        return False
    if players[player]["discord_account"] == "None":
        return False
    return True

def get_linked(player: str):
    global players
    if player not in players:
        return None
    return players[player]["discord_account"]