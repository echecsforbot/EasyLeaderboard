import discord
from discord.ext import commands
from discord import app_commands
import importlib
from typing import Literal
import os
import json
import shutil

ermg = importlib.import_module("tools.errors_manager")
dtmg = importlib.import_module("tools.data_manager")
uffx = importlib.import_module("tools.usefull_fx")
cfg = importlib.import_module("tools.config")

class Export(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="export", description="Export the database (devs allowed)")
    @app_commands.guilds(discord.Object(id=cfg.guild_id))
    async def export(self, interaction: discord.Interaction, format: Literal["json", "zip"]):
        if ermg.UserExistCheck(interaction.user.id):
            if interaction.guild.get_role(cfg.admins) not in interaction.user.roles and interaction.guild.get_role(cfg.devs) not in interaction.user.roles:
                return

            embed = discord.Embed(color=cfg.system_color)
            embed.add_field(name=f"Starting to export...", value="")
            await interaction.response.send_message(embed=embed)

            embed = discord.Embed(color=cfg.system_color)
            embed.add_field(name=f"Export finished!", value="")

            if format == "json":
                file_content = {}
                for file in os.listdir(f"../{cfg.project_name}/users/"):
                    file_name = str(os.fsdecode(file))

                    file_content[file_name[:-5]] = dtmg.read_json(f"../{cfg.project_name}/users/{file_name}")

                newdata_content = json.dumps(file_content, indent=len(os.listdir(f"../{cfg.project_name}/users/")))
                with open(f"../{cfg.project_name}/{cfg.bot_name}_db_export.json", "w", encoding = "utf-8") as DBF:
                    DBF.write(newdata_content)

                await interaction.followup.send(embed=embed, file=discord.File(f"../{cfg.project_name}/{cfg.bot_name}_db_export.json"))

            else:
                shutil.copytree(f"../{cfg.project_name}/users/", f"../{cfg.project_name}/{cfg.bot_name}_db_export/", dirs_exist_ok=True)
                shutil.make_archive(f"{cfg.bot_name}_db_export", "zip", root_dir=f"../{cfg.project_name}", base_dir=f"{cfg.bot_name}_db_export")

                await interaction.followup.send(embed=embed, file=discord.File(f"../{cfg.project_name}/{cfg.bot_name}_db_export.zip"))
                
        else:
            await interaction.response.send_message(embed=ermg.UserExistEmbed())

        
async def setup(bot) -> None:
    await bot.add_cog(Export(bot), override=True)