import discord
from discord.ext import commands
from discord import app_commands
import importlib
from typing import Literal
import time

ermg = importlib.import_module("tools.errors_manager")
dtmg = importlib.import_module("tools.data_manager")
uffx = importlib.import_module("tools.usefull_fx")
cfg = importlib.import_module("tools.config")

class Undo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="undo", description="Cancel your last win")
    @app_commands.guilds(discord.Object(id=cfg.guild_id))
    async def undo(self, interaction: discord.Interaction, game: Literal["Territorial", "OpenFront"]):
        if ermg.UserExistCheck(interaction.user.id):

            dbvar = dtmg.read_json(f"../{cfg.project_name}/dbvar.json")
            user_data = dtmg.read_json(f"../{cfg.project_name}/users/{interaction.user.id}.json")

            gamedict = {"Territorial": "tt", "OpenFront": "of"}
            points_types = ["season_pts", "alltime_pts"]
            last_pts = user_data[gamedict[game]]["last_pts"]

            for point_type in points_types:
                dtmg.ChangeData(interaction.user.id, "add", - last_pts, gamedict[game], point_type)
            if dbvar["event"] == 1:
                dtmg.ChangeData(interaction.user.id, "add", - last_pts, gamedict[game], "event_pts")
            
            dtmg.ChangeData(interaction.user.id, "set", 0, gamedict[game], "last_pts")
            with open(f"../{cfg.project_name}/users_log/{interaction.user.id}.txt", "a") as UFL:
                UFL.write(f"{round(time.time())},{gamedict[game]},{- last_pts}")
            
            embed = discord.Embed(color=cfg.color)
            embed.add_field(name=f"You canceled your last win on {game} and removed yourself {last_pts} points.", value="")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(embed=ermg.UserExistEmbed())

        
async def setup(bot) -> None:
    await bot.add_cog(Undo(bot), override=True)