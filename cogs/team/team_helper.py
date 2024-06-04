import datetime
import requests
import discord
import json

from config import config as config_main
import cogs.util.util_helper as util_helper

config = config_main["team"]

def get_server_team(guild_id: discord.guild.Guild):
    return util_helper.get_team(guild_id)

def get_team_check(team_name: str):
    if not util_helper.check_team(team_name):
        return None
    return team_name

def get_stats(team_name: str):
    stats = requests.get(f"https://collegefootballrisk.com/api/team?team={team_name}")
    if not stats:
        return None
    stats = stats.json()
    return {
        "team": stats["team"],
        "territories": stats["territories"],
        "players": stats["players"],
        "total_stars": stats["stars"],
        "mercs": stats["mercs"],
    }

def roster(team_name: str):
    roster = requests.get(f"https://collegefootballrisk.com/api/players?team={team_name}")
    if not roster:
        return None
    roster = roster.json()
    player_list = []
    for player in roster:
        player_list.append(player["player"])
    return player_list


def team_not_found():
    embed = discord.Embed(
        title="Team not found",
        description="Team not found, please try again.",
        color=discord.Color.red(),
        timestamp=datetime.datetime.now(),
    )
    return embed