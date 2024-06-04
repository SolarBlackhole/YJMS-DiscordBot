import discord
import asyncio
from discord.ext import commands
from discord import app_commands
import datetime
import cogs.team.team_helper as team_helper

class team(commands.GroupCog, name="team"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        team_helper.setup()
        print("teamSetup cog loaded!")

    @app_commands.command(
        name="stats",
        description="Get a team's stats, defults the server's team if not provided.",
    )
    async def stats(self,
                    interaction: discord.Interaction,
                    team_name: str = None,
    ):
        if not team_name:
            team_name = team_helper.get_server_team(interaction.guild_id)
            if not team_name:
                embed = discord.Embed(
                    title="No team set",
                    description="No team set for this server, please set one.",
                    color=discord.Color.red(),
                    timestamp=datetime.datetime.now(),
                )
                await interaction.response.send_message(embed=embed)
                return
        else:
            team_name = team_helper.get_team_check(team_name)
            if not team_name:
                await interaction.response.send_message(embed=team_helper.team_not_found())
                return
        
        await interaction.response.defer(ephemeral=True, thinking=True)
        await asyncio.sleep(3)

        stats = team_helper.get_stats(team_name)
        
        embed = discord.Embed(
            title=f"Stats for {team_name}",
            description=f"Territories: {stats['territories']}\nPlayers: {stats['players']}\nTotal Stars: {stats['total_stars']}\nMercs: {stats['mercs']}",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now(),
        )
        await interaction.followup.send(
            content= None,
            embed=embed,
            ephemeral=False,
        )
        
    
    @app_commands.command(
        name="roster",
        description="Get a team's roster, defults the server's team if not provided.",
    )
    async def roster(self,
                    interaction: discord.Interaction,
                    team_name: str = None,
    ):
        if not team_name:
            team_name = team_helper.get_server_team(interaction.guild_id)
            if not team_name:
                embed = discord.Embed(
                    title="No team set",
                    description="No team set for this server, please set one.",
                    color=discord.Color.red(),
                    timestamp=datetime.datetime.now(),
                )
                await interaction.response.send_message(embed=embed)
                return
        else:
            team_name = team_helper.get_team_check(team_name)
            if not team_name:
                await interaction.response.send_message(embed=team_helper.team_not_found())
                return
        roster = team_helper.roster(team_name)
        if not roster:
            embed = discord.Embed(
                title=f"{team_name} has no players",
                description="This team has no current players.",
                color=discord.Color.red(),
                timestamp=datetime.datetime.now(),
            )
            await interaction.response.send_message(embed=embed)
            return
        embed = discord.Embed(
            title=f"Roster for {team_name}",
            description="\n".join(roster),
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now(),
        )
        await interaction.response.send_message(embed=embed)