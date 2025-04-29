import discord
from discord.ext import commands
from discord import app_commands
import importlib
from typing import Literal
import time
import json

ermg = importlib.import_module("tools.errors_manager")
dtmg = importlib.import_module("tools.data_manager")
uffx = importlib.import_module("tools.usefull_fx")
cfg = importlib.import_module("tools.config")

class Add(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="add", description="Update your score")
    @app_commands.guilds(discord.Object(id=cfg.guild_id))
    async def add(self, interaction: discord.Interaction, game: Literal["Territorial", "OpenFront"], points:app_commands.Range[float, -4096, 1024]):
        if ermg.UserExistCheck(interaction.user.id):
            #POINTS
            gamedict = {"Territorial": "tt", "OpenFront": "of"}
            dbvar = dtmg.read_json(f"../{cfg.project_name}/dbvar.json")
            user_data = dtmg.read_json(f"../{cfg.project_name}/users/{interaction.user.id}.json")
            points_types = ["season_pts", "alltime_pts"]

            if int(points) > 0:
                true_pts = int(round(points * dbvar["base_multi"] * dbvar["boost_multi"]))
            else:
                true_pts = int(round(points))

            if user_data[gamedict[game]]["season_pts"] + true_pts <= 0:
                true_pts = -user_data[gamedict[game]]["season_pts"]

            dtmg.ChangeData(interaction.user.id, "set", true_pts, gamedict[game], "last_pts")

            for point_type in points_types:
                dtmg.ChangeData(interaction.user.id, "add", true_pts, gamedict[game], point_type)
            if dbvar["event"] == 1:
                dtmg.ChangeData(interaction.user.id, "add", true_pts, gamedict[game], "event_pts")

            with open(f"../{cfg.project_name}/users_log/{interaction.user.id}.txt", "a") as UFL:
                UFL.write(f"\n{round(time.time())},{gamedict[game]},{true_pts},")

            #RESPONSE
            embed = discord.Embed(color=cfg.color)
            value = f"{cfg.pts_ico} {uffx.QuantityToText(true_pts, cfg.sep_char)}"

            if dbvar["boost_multi"] != 1:
                embed.add_field(name=f":tada: {user_data['name']} won a {game} game and gained some points, multiplied by a x{dbvar['boost_multi']} event boost!", value=value)
            else:
                embed.add_field(name=f"{user_data['name']} won a {game} game and gained some points:", value=value)

            await interaction.response.send_message(embed=embed)


            #FIRST
            if true_pts + user_data[gamedict[game]]["season_pts"] > dbvar[f"{gamedict[game]}_first_pts"]:
                old_first = await self.bot.fetch_user(dbvar[f"{gamedict[game]}_first"])
                dbvar_update = dbvar

                if cfg.tt_first != None and gamedict[game] == "tt":
                    interaction.guild.get_role(cfg.tt_first)
                    await old_first.remove_roles(cfg.tt_first)
                    await interaction.user.add_roles(cfg.tt_first)

                elif cfg.of_first != None and gamedict[game] == "of":
                    interaction.guild.get_role(cfg.of_first)
                    await old_first.remove_roles(cfg.of_first)
                    await interaction.user.add_roles(cfg.of_first)

                dbvar[f"{gamedict[game]}_first"] = interaction.user.id
                dbvar[f"{gamedict[game]}_first_pts"] = true_pts + user_data[gamedict[game]]["season_pts"]
                embed = discord.Embed(color=cfg.color)

                dbvar_update[f"{gamedict[game]}_first"] = interaction.user.id
                dbvar_update[f"{gamedict[game]}_first_pts"] = true_pts + user_data[gamedict[game]]["season_pts"]

                newdata_content = json.dumps(dbvar_update, indent=7)
                with open(f"../{cfg.project_name}/dbvar.json", "w", encoding = "utf-8") as DBF:
                    DBF.write(newdata_content)

            #RANKS
            if gamedict[game] == "tt":
                ranks = cfg.ranks_tt
            else:
                ranks = cfg.ranks_of

            role_added = False
            embed = discord.Embed(color=cfg.color)
            for rank in ranks:
                role = discord.utils.get(interaction.guild.roles, name=f"{ranks[rank][0]}")

                if role not in interaction.user.roles and points + user_data[gamedict[game]]["season_pts"] >= ranks[rank][0]:
                    role_added = True

                    await interaction.user.add_roles(role)

                    message = f"You unlocked a new rank: you are now **{ranks[rank][0]}**! Thanks for grinding and keep up the good work."
                    embed.add_field(name=":partying_face: Congratulations!", value=message)

            if role_added:
                await interaction.followup.send(embed=embed)

        else:
            await interaction.response.send_message(embed=ermg.UserExistEmbed())

        
async def setup(bot) -> None:
    await bot.add_cog(Add(bot), override=True)