import discord
from discord.ext import commands
from discord import app_commands
import importlib
from typing import Literal
import json
import os
import time

ermg = importlib.import_module("tools.errors_manager")
dtmg = importlib.import_module("tools.data_manager")
uffx = importlib.import_module("tools.usefull_fx")
cfg = importlib.import_module("tools.config")

class Event(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="event", description="Manage events")
    @app_commands.guilds(discord.Object(id=cfg.guild_id))
    async def event(self, interaction: discord.Interaction, status: Literal["On", "Off", "Reset"]):        
        if ermg.UserExistCheck(interaction.user.id):
            if interaction.guild.get_role(cfg.admins) not in interaction.user.roles:
                return
            
            embed = discord.Embed(color=cfg.system_color)
            dbvar = dtmg.read_json(f"dbvar.json")

            on_off = {"Off": 0, "On": 1}
            dbvar["event"] = on_off[status]

            newdata_content = json.dumps(dbvar, indent=7)
            with open(f"../{cfg.project_name}/dbvar.json", "w", encoding = "utf-8") as DBF:
                DBF.write(newdata_content)

            embed = discord.Embed(color=cfg.system_color)

            content = ""
            if status == "Reset":
                games = ["of", "tt"]

                for file in os.listdir(f"../{cfg.project_name}/users/"):
                    file_name = str(os.fsdecode(file))
                    user_data = dtmg.read_json(f"../{cfg.project_name}/users/{file_name}")

                    for game in games:
                        user_data[game]["event_pts"] = 0

                    newdata_content = json.dumps(user_data, indent=3)
                    with open(f"../{cfg.project_name}/users/{file_name}", "w") as UF:
                        UF.write(newdata_content)

            
                embed.add_field(name="Event leaderboard was erased")

            else:
                embed.add_field(name=f"Event set to {status}", value="")
                
            await interaction.response.send_message(embed=embed)
            
        else:
            await interaction.response.send_message(embed=ermg.UserExistEmbed())

        
async def setup(bot) -> None:
    await bot.add_cog(Event(bot), override=True)