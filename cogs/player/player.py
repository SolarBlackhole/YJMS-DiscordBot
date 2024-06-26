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
                    player_name: str,
    ):
        player_name = player_helper.search_player(player_name)
        info = player_helper.get_info(player_name)
        if not info:
            await interaction.response.send_message(embed=player_helper.player_not_found())
            return
        embed = discord.Embed(
            title=f"Info for {player_name}",
            description=f"Stars: {info['stars']}\nTotal Turns: {info['totalTurns']}\nGame Turns: {info['gameTurns']}\nMVPs: {info['mvps']}\nStreak: {info['streak']}\nPlatform: {info['platform']}",
            color=discord.Color.blue(),
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="add",
        description="Add a player to the database",
    )
    async def add(self, 
                    interaction: discord.Interaction, 
                    player_name: str,
                    discord_name: discord.member.Member = None,
    ):
        if player_helper.player_check(player_name):
            if player_helper.is_linked(player_name):
                embed = discord.Embed(
                    title="Player already in database",
                    description=f"{player_name} is already in the database and is linked to discord user {player_helper.get_linked(player_name)}",
                    color=discord.Color.red(),
                )
                await interaction.response.send_message(embed=embed)
                return
            embed = discord.Embed(
                title="Player already in database",
                description=f"{player_name} is already in the database. If you would like to link a discord account to this player, use the link command.",
                color=discord.Color.red(),
            )
            await interaction.response.send_message(embed=embed)
            return
        info = player_helper.get_info(player_name)
        if not info:
            await interaction.response.send_message(embed=player_helper.player_not_found())
            return
        player_helper.player_add(player_name, discord_name)
        await interaction.response.send_message("Player added to database")

    @app_commands.command(
        name="remove",
        description="Remove a player from the database",
    )
    async def remove(self, 
                    interaction: discord.Interaction, 
                    player_name: str,
    ):
        success = player_helper.player_remove(player_name)
        if not success:
            await interaction.response.send_message(embed=player_helper.player_not_found())
            return
        embed = discord.Embed(
            title="Player removed",
            description=f"{player_name} has been removed from the database",
            color=discord.Color.green(),
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="link",
        description="Link a player to a discord account",
    )
    async def link(self,
                    interaction: discord.Interaction,
                    player_name: str,
                    discord_name: discord.member.Member,
    ):
        Success = player_helper.player_link(player_name, discord_name)
        print(f"Success: {Success}")
        if not Success:
            await interaction.response.send_message(embed=player_helper.player_not_found())
            return
        embed = discord.Embed(
            title="Player linked",
            description=f"{player_name} has been linked to {discord_name}",
            color=discord.Color.green(),
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(playerSetup(bot))