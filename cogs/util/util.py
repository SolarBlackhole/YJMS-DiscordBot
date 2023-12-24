import discord
import json
from discord import app_commands
from discord.ext import commands
from discord.utils import get

import cogs.util.util_helper as util_helper
from config import config as config_main

config = config_main["util"]

@app_commands.guild_only()
class UtilSetup(commands.Cog):
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
        
        
  

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UtilSetup(bot))