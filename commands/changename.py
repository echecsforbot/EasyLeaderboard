import discord
from discord.ext import commands
from discord import app_commands
import importlib
from typing import Literal

ermg = importlib.import_module("tools.errors_manager")
uffx = importlib.import_module("tools.usefull_fx")
dtmg = importlib.import_module("tools.data_manager")
cfg = importlib.import_module("tools.config")

class ChangeName(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="changename", description="Change your username")
    @app_commands.guilds(discord.Object(id=cfg.guild_id))
    async def changename(self, interaction: discord.Interaction, username:app_commands.Range[str, 3, 20]):
        if ermg.UserExistCheck(interaction.user.id):
            if ermg.ValidNameCheck(username):
                dtmg.ChangeData(interaction.user.id, "set", username, "name")

                embed = discord.Embed(color=cfg.system_color)
                embed.add_field(name=f"Your new username is {username}", value="", inline=False)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(embed=ermg.ValidNameEmbed())
            
        else:
            await interaction.response.send_message(embed=ermg.UserExistEmbed())

        
async def setup(bot) -> None:
    await bot.add_cog(ChangeName(bot), override=True)