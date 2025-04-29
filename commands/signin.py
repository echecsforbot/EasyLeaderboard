import discord
from discord.ext import commands
from discord import app_commands
import importlib

ermg = importlib.import_module("tools.errors_manager")
uffx = importlib.import_module("tools.usefull_fx")
cfg = importlib.import_module("tools.config")

class Signin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="signin", description="Register yourself into the database")
    @app_commands.guilds(discord.Object(id=cfg.guild_id))
    async def signin(self, interaction: discord.Interaction, username: app_commands.Range[str, 3, 20]):
        if not ermg.UserExistCheck(interaction.user.id):
            if ermg.ValidNameCheck(username):
                uffx.CreateUser(interaction.user, username)

                embed = discord.Embed(color=cfg.system_color)
                embed.add_field(name=f"You successfully registered yourself as {username} into the database!", value="", inline=False)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(embed=ermg.ValidNameEmbed())
        else:
            await interaction.response.send_message(embed=ermg.AccountExistEmbed())

        
async def setup(bot) -> None:
    await bot.add_cog(Signin(bot), override=True)