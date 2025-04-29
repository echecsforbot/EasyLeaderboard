import discord
from discord.ext import commands
import os
import datetime
import asyncio
import tools.config as cfg

bot_intents = discord.Intents.default()
bot_intents.message_content = True
bot = commands.Bot(command_prefix = "/", 
                   activity = discord.Game(name = cfg.activity), 
                   intents = bot_intents,
                   help_command=None)

@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=cfg.guild_id))
    now = datetime.datetime.now()
    print("-" * 64)
    print(f"{str(now)[:19]} - {cfg.bot_name} is online.")
    print("-" * 64)
    
async def LoadCogs():
    for file in os.listdir(f"../{cfg.project_name}/commands/"):
        if file.endswith(".py"):
            await bot.load_extension(f"commands.{file[:-3]}")
            now = datetime.datetime.now()
            print(f"{str(now)[:19]} - commands.{file[:-3]} loaded")

async def main():
    print("#" * 64)
    await LoadCogs()
    await bot.start(cfg.token)

asyncio.run(main())