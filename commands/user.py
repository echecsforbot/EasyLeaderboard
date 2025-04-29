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

class User(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="user", description="Manage users")
    @app_commands.guilds(discord.Object(id=cfg.guild_id))
    async def user(self, interaction: discord.Interaction, action:Literal["set", "reset", "add"], target:str, game: Literal["Territorial", "OpenFront", "All"], points:float):
        if ermg.UserExistCheck(interaction.user.id):
            if interaction.guild.get_role(cfg.admins) not in interaction.user.roles:
                return
            
            else:
                target_id = int(target[2:-1])
                gamedict = {"Territorial": "tt", "OpenFront": "of"}
                dbvar = dtmg.read_json(f"../{cfg.project_name}/dbvar.json")
                user_data = dtmg.read_json(f"../{cfg.project_name}/users/{target_id}.json")

                if int(points) > 0:
                    true_pts = int(round(points * dbvar["base_multi"] * dbvar["boost_multi"]))
                else:
                    true_pts = int(round(points))


                if game == "All":
                    games = [value for value in gamedict.values()]
                else:
                    games = [gamedict[game]]
                

                for game_type in range(len(games)):
                    if action == "add":
                        with open(f"../{cfg.project_name}/users_log/{target_id}.txt", "a") as UFL:
                            UFL.write(f"\n{round(time.time())},{games[game_type]},{true_pts},")

                        dtmg.ChangeData(target_id, "add", true_pts, games[game_type], "alltime_pts")
                        dtmg.ChangeData(target_id, "add", true_pts, games[game_type], "season_pts")

                        if dbvar["event"] == 1:
                            dtmg.ChangeData(target_id, "add", true_pts, games[game_type], "event_pts")


                    elif action in ["set", "reset"]:
                        if action == "reset":
                            true_pts = 0

                        with open(f"../{cfg.project_name}/users_log/{target_id}.txt", "a") as UFL:
                            UFL.write(f"\n{round(time.time())},{games[game_type]},{true_pts - user_data[games[game_type]]['season_pts']},")

                        dtmg.ChangeData(target_id, "set", true_pts, games[game_type], "season_pts")
                        dtmg.ChangeData(target_id, "add", true_pts - user_data[games[game_type]]['season_pts'], games[game_type], "alltime_pts")
                        
                        if dbvar["event"] == 1:
                            dtmg.ChangeData(target_id, "add", true_pts - user_data[games[game_type]]['season_pts'], games[game_type], "event_pts")


                
                embed = discord.Embed(color=cfg.admin_color)
                value = f"{cfg.pts_ico} {uffx.QuantityToText(true_pts, cfg.sep_char)}"
                embed.add_field(name=f"{interaction.user.name}:\nTarget: {target}\nAction: {action}\nPoints: {value}\nGame: {game}", value="")

                await interaction.response.send_message(embed=embed)

        else:
            await interaction.response.send_message(embed=ermg.UserExistEmbed())

        
async def setup(bot) -> None:
    await bot.add_cog(User(bot), override=True)