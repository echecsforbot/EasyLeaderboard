import discord
from discord.ext import commands
from discord import app_commands
import importlib
from typing import Literal

ermg = importlib.import_module("tools.errors_manager")
dtmg = importlib.import_module("tools.data_manager")
uffx = importlib.import_module("tools.usefull_fx")
cfg = importlib.import_module("tools.config")

class Profile(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="profile", description="Look at someone's profile")
    @app_commands.guilds(discord.Object(id=cfg.guild_id))
    async def profile(self, interaction: discord.Interaction, user:str | None):
        if ermg.UserExistCheck(interaction.user.id):
            embed = discord.Embed(color=cfg.color)
            if user == None:
                target = interaction.user
            else:
                target = await self.bot.fetch_user(int(user[2:-1]))

            try:
                user_data = dtmg.read_json(f"../{cfg.project_name}/users/{target.id}.json")
            except:
                embed.add_field(name="", value="This user has not registered yet.")
                await interaction.response.send_message(embed=embed)
                return
            
            games = {"Territorial": "tt", "OpenFront": "of"}
            embed.set_thumbnail(url=target.avatar)
            embed.add_field(name=f"{user_data['name']}'s profile", value="", inline=False)
            for game in games.keys():
                embed.add_field(name=game, value=f"All time ⠂{uffx.QuantityToText(user_data[games[game]]['alltime_pts'], cfg.sep_char)}\nSeason ⠂{uffx.QuantityToText(user_data[games[game]]['season_pts'], cfg.sep_char)}\nEvent ⠂{uffx.QuantityToText(user_data[games[game]]['event_pts'], cfg.sep_char)}", inline=True)

            await interaction.response.send_message(embed=embed)
            
        else:
            await interaction.response.send_message(embed=ermg.UserExistEmbed())

        
async def setup(bot) -> None:
    await bot.add_cog(Profile(bot), override=True)