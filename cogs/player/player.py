import discord
from discord.ext import commands
from discord import app_commands

import cogs.player.player_helper as player_helper

class playerSetup(commands.GroupCog, name="player"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        player_helper.setup()
        print("playerSetup cog loaded!")

    @app_commands.command(
        name="info",
        description="Get a player's info",
    )
    async def info(self, 
                    interaction: discord.Interaction, 
                    reddit_name: str,
    ):
        reddit_name = reddit_name.lower()
        info = player_helper.get_info(reddit_name)
        if not info:
            await interaction.response.send_message("Either the player is not found or the API is down")
            return
        embed = discord.Embed(
            title=f"Info for {reddit_name}",
            description=f"Stars: {info['stars']}\nTotal Turns: {info['totalTurns']}\nGame Turns: {info['gameTurns']}\nMVPs: {info['mvps']}\nStreak: {info['streak']}",
            color=discord.Color.blue(),
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="add",
        description="Add a player to the database",
    )
    async def add(self, 
                    interaction: discord.Interaction, 
                    reddit_name: str,
                    discord_name: discord.member.Member = None,
    ):
        reddit_name = reddit_name.lower()
        if player_helper.player_check(reddit_name):
            await interaction.response.send_message("Player already in database")
            return
        player_helper.player_add(reddit_name, discord_name)
        await interaction.response.send_message("Player added to database")

    @app_commands.command(
        name="remove",
        description="Remove a player from the database",
    )
    async def remove(self, 
                    interaction: discord.Interaction, 
                    reddit_name: str,
    ):
        reddit_name = reddit_name.lower()
        if not player_helper.player_check(reddit_name):
            await interaction.response.send_message("Player not in database")
            return
        player_helper.player_remove(reddit_name)
        await interaction.response.send_message("Player removed from database")

    @app_commands.command(
        name="link",
        description="Link a player to a discord account",
    )
    async def link(self,
                    interaction: discord.Interaction,
                    reddit_name: str,
                    discord_name: discord.member.Member,
    ):
        reddit_name = reddit_name.lower()
        if not player_helper.player_check(reddit_name):
            await interaction.response.send_message("Player not in database")
            return
        player_helper.player_link(reddit_name, discord_name)
        await interaction.response.send_message("Player linked to discord account")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(playerSetup(bot))
