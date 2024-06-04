import discord
import json
import datetime
from discord import app_commands
from discord.ext import commands
from discord.utils import get

import cogs.util.util_helper as util_helper
from config import config as config_main

config = config_main["util"]

@app_commands.guild_only()
class Util(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        util_helper.setup(self.bot.guilds)
        print("UtilSetup cog loaded!")

    

    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sync(self, ctx):
        print("Syncing")
        await self.bot.tree.sync()
        print("Synced")
        await ctx.send("Synced")

    @app_commands.command(
        name="team",
        description="Set this server's team",
    )
    async def team(self,
                    interaction: discord.Interaction,
                    team: str,
    ):
        have_team = util_helper.team_check(interaction.guild_id)
        if have_team:
            embed = discord.Embed(
                title="Team already set",
                description=f"This server already has a team set ({util_helper.get_team(interaction.guild_id)}). Would you like to change it?",
                color=discord.Color.yellow(),
                timestamp=datetime.datetime.now(),
            )
            view = util_helper.change_button()
            await interaction.response.send_message(embed=embed, view=view)
            message = await interaction.original_response()
            view.message = message
            timeout = await view.wait()

            if timeout is True:
                await message.edit(embed=discord.Embed(
                    title="Timed out",
                    description="You took too long to respond. Please try again.",
                    color=discord.Color.blue(),
                    timestamp=datetime.datetime.now(),
                ))
            elif view.remove:
                sucess = util_helper.team_set(interaction.guild_id, team)
                if not sucess:
                    await message.edit(embed=util_helper.team_not_found())
                    return
                embed = discord.Embed(
                    title=f"Set team to {team}",
                    color=discord.Color.blue(),
                    timestamp=datetime.datetime.now(),
                )
                await message.edit(embed=embed)
            else:
                embed = discord.Embed(
                    title="Cancelled",
                    description="Cancelled the team change.",
                    color=discord.Color.blue(),
                    timestamp=datetime.datetime.now(),
                )
                await message.edit(embed=embed)
            return

        sucess = util_helper.team_set(interaction.guild_id, team)
        if not sucess:
            await interaction.response.send_message(embed=util_helper.team_not_found())
            return
        embed = discord.Embed(
            title=f"Set team to {team}",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now(),
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="playing",
        description="Set if this server is playing",
    )
    async def playing(self,
                    interaction: discord.Interaction,
                    playing: bool,
    ):
        util_helper.set_playing(interaction.guild_id, playing)
        embed = discord.Embed(
            title=f"Set playing to {playing}",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now(),
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="get_team",
        description="Get this server's team",
    )
    async def get_team(self,
                    interaction: discord.Interaction,
    ):
        team = util_helper.get_team(interaction.guild_id)
        embed = discord.Embed(
            title=f"Team for this server",
            description=f"Team: {team}",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now(),
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Util(bot))