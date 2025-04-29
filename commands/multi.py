import discord
from discord.ext import commands
from discord import app_commands
import importlib
from typing import Literal
import json

ermg = importlib.import_module("tools.errors_manager")
dtmg = importlib.import_module("tools.data_manager")
uffx = importlib.import_module("tools.usefull_fx")
cfg = importlib.import_module("tools.config")

class Multi(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="multi", description="Staff only")
    @app_commands.guilds(discord.Object(id=cfg.guild_id))
    async def multi(self, interaction: discord.Interaction, multi: Literal["base", "boost"], value: float):
        if ermg.UserExistCheck(interaction.user.id):
            if interaction.guild.get_role(cfg.admins) not in interaction.user.roles:
                return
            
            try:
                if int(round(value)) == value:
                    value = int(value)
            except:
                pass

            embed = discord.Embed(color=cfg.system_color)
            dbvar = dtmg.read_json(f"../{cfg.project_name}/dbvar.json")
            dbvar[f"{multi}_multi"] = value

            newdata_content = json.dumps(dbvar, indent=7)
            with open(f"dbvar.json", "w", encoding = "utf-8") as DBF:
                DBF.write(newdata_content)

            embed.add_field(name=f"{multi[0].upper()}{multi[1:]} multi set to x{uffx.QuantityToText(value, cfg.sep_char)}", value="*To set it off: set it up to 1*")

            await interaction.response.send_message(embed=embed)
            
        else:
            await interaction.response.send_message(embed=ermg.UserExistEmbed())

        
async def setup(bot) -> None:
    await bot.add_cog(Multi(bot), override=True)