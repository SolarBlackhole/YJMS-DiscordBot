import json
import discord
import requests
import datetime
from config import config as config_main

config = config_main["util"]

teams = {}

debug = False

def setup(guilds: list[discord.guild.Guild]):
    global teams

    try:
        with open(config["save_location"] + "util.json") as f:
            pass
        f.close()
    except IOError as e:
        print("Util file not found... Making it now")
        f = open(config["save_location"] + "util.json", "w")
        f.write("{}")
        f.close()

    with open(config["save_location"] + "util.json") as f:
        teams = json.load(f)
    
    for guild in guilds:
        if str(guild.id) not in teams.keys():
            teams[str(guild.id)] = {"playing": False, "team": "None"}

    save()

    f.close()

def save():
    global teams

    with open(config["save_location"] + "util.json", "w") as f:
        if debug:
            json.dump(
                teams,
                f,
                indent=4,
                sort_keys=True,
                separators=(",", ": "),
            )
        else:
            json.dump(teams, f)
    f.close()

def team_check(guild_id: discord.guild.Guild):
    global teams

    if teams[str(guild_id)]["team"] != "None":
        return True
    return False

def team_set(guild_id: discord.guild.Guild, team: str):
    global teams

    if not check_team(team):
        return False
    teams[str(guild_id)]["team"] = team
    save()

def check_team(team: str):
    team_list = requests.get(f"https://collegefootballrisk.com/api/teams")
    if not team_list:
        return False
    teams = team_list.json()
    if team in teams:
        return True
    return False

def get_team(guild_id: discord.guild.Guild):
    global teams
    
    if teams[str(guild_id)]["team"] == "None":
        return None
    return teams[str(guild_id)]["team"]

def get_playing(guild_id: discord.guild.Guild):
    global teams

    return teams[str(guild_id)]["playing"]

def set_playing(guild_id: discord.guild.Guild, playing: bool):
    global teams

    teams[str(guild_id)]["playing"] = playing
    save()

def team_not_found():
    return discord.Embed(
        title="Team not found",
        description="The team you entered was not found. Please try again.",
        color=discord.Color.red(),
        timestamp=datetime.datetime.now(),
    )

class change_button(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=30)
        
        remove: bool = None

        @discord.ui.button(
                label="Change", style=discord.ButtonStyle.primary
        )
        async def change(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.remove = True
            button.disabled = True
            button1 = [i for i in self.children if i.custom_id == "cancel"][0]
            button1.disabled = True
            await interaction.response.edit_message(view=self)
            self.stop()
        
        @discord.ui.button(
             label="Cancel", style=discord.ButtonStyle.grey, custom_id="cancel"
        )
        async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.remove = False
            button.disabled = True
            button1 = [i for i in self.children if i.custom_id == "change"][0]
            button1.disabled = True
            await interaction.response.edit_message(view=self)
            self.stop()

        async def on_timeout(self):
            button = [i for i in self.children if i.custom_id == "change"][0]
            button.disabled = True
            button = [i for i in self.children if i.custom_id == "cancel"][0]
            button.disabled = True
            await self.message.edit(view=self)