import discord
from discord.ext import commands
from discord import app_commands
import importlib
import os
import json
import time

ermg = importlib.import_module("tools.errors_manager")
dtmg = importlib.import_module("tools.data_manager")
uffx = importlib.import_module("tools.usefull_fx")
cfg = importlib.import_module("tools.config")

class Reset(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="reset", description="Staff only")
    @app_commands.guilds(discord.Object(id=cfg.guild_id))
    async def reset(self, interaction: discord.Interaction, passcode: int):
        if ermg.UserExistCheck(interaction.user.id):
            if interaction.guild.get_role(cfg.admins) not in interaction.user.roles:
                return
            
            embed = discord.Embed(color=cfg.system_color)
            if passcode != cfg.passcode:
                embed.add_field(name="Wrong passcode", value ="")
                await interaction.response.send_message(embed=embed)

            else:
                embed.add_field(name="Reset starting...", value ="")
                await interaction.response.send_message(embed=embed)

                points_types = ["season_pts", "event_pts", "last_pts"]
                games = ["of", "tt"]

                #user.json
                for file in os.listdir(f"../{cfg.project_name}/users/"):
                    file_name = str(os.fsdecode(file))
                    user_data = dtmg.read_json(f"../{cfg.project_name}/users/{file_name}")

                    for game in games:
                        for point_type in points_types:
                            user_data[game][point_type] = 0

                    newdata_content = json.dumps(user_data, indent=3)
                    with open(f"../{cfg.project_name}/users/{file_name}", "w") as UF:
                        UF.write(newdata_content)

                #user.txt
                for file in os.listdir(f"../{cfg.project_name}/users_log/"):
                    file_name = str(os.fsdecode(file))
                    
                    now = round(time.time())
                    with open(f"../{cfg.project_name}/users_log/{file_name}", "w") as UF:
                        UF.write(f"{now},of,0,\n{now},tt,0,")

                #dbvar.json and first
                dbvar = dtmg.read_json(f"../{cfg.project_name}/dbvar.json")
                dbvar_update = dbvar

                if cfg.tt_first != None and dbvar["tt_first"] != 0:
                    interaction.guild.get_role(cfg.tt_first)
                    old_first = await self.bot.fetch_user(dbvar["tt_first"])
                    await old_first.remove_roles(cfg.tt_first)

                if cfg.of_first != None and dbvar["of_first"] != 0:
                    interaction.guild.get_role(cfg.of_first)
                    old_first = await self.bot.fetch_user(dbvar["of_first"])
                    await old_first.remove_roles(cfg.of_first)

                for game in ["of", "tt"]:
                    dbvar_update[f"{game}_first"] = 0
                    dbvar_update[f"{game}_first_pts"] = 0

                newdata_content = json.dumps(dbvar_update, indent=7)
                with open(f"../{cfg.project_name}/dbvar.json", "w", encoding = "utf-8") as DBF:
                    DBF.write(newdata_content)

                embed = discord.Embed(color=cfg.system_color)
                embed.add_field(name="Reset finished!", value ="")
                await interaction.followup.send(embed=embed)
            
        else:
            await interaction.response.send_message(embed=ermg.UserExistEmbed())

        
async def setup(bot) -> None:
    await bot.add_cog(Reset(bot), override=True)