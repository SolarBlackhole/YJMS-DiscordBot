import discord
from discord.ext import commands
from secret import application_id, bot_token
from config import config


class MyBot(commands.Bot):
    async def setup_hook(self):
        for ext in config["cogs"]:
            await self.load_extension(ext)

    async def on_ready(self):
        await self.wait_until_ready()
        await self.change_presence(activity=discord.Game(name="College Football Risk"))
        print(f"{self.user} has connected to Discord!")

        
bot = MyBot(
    command_prefix=config["command_prefix"],
    intents=discord.Intents.all(),
    application_id=application_id,
)

bot.run(bot_token)