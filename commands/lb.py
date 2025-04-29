import discord
from discord.ext import commands
from discord import app_commands
import importlib
from typing import Literal
import os
import math
import time

ermg = importlib.import_module("tools.errors_manager")
dtmg = importlib.import_module("tools.data_manager")
uffx = importlib.import_module("tools.usefull_fx")
cfg = importlib.import_module("tools.config")

def PageEmbed(lb, page:int, game:str, span:str):
    embed = discord.Embed(color=cfg.color)
    if span in ["week", "day", "event", "alltime", "season"]:
        span_display = f"({span})"
    else:
        span_display = f"({span} days)"


    embed.add_field(name=f":trophy: Leaderboard  ⠂{game} {span_display}", value="", inline=False)
    lb_index = len(lb) - (15 * page)

    page_mod = 15 * (page - 1)

    if len(lb) == 0:
        embed.add_field(name="", value="No one is in this leaderboard yet.", inline=False)
    else:
        if lb_index <= 0:
            page_users = [(user[0], user[1]) for user in lb]
        elif lb_index <= 14:
            page_users = lb[page_mod:page_mod + lb_index]
        else:
            page_users = lb[page_mod:page_mod + 15]

        top_emoji = ["first", "second", "third"]

        content = ""
        for user in range(len(page_users)):
            if page == 1 and user in range(3):
                content = content + f":{top_emoji[user]}_place: **{page_users[user][0]}** ⠂{uffx.QuantityToText(page_users[user][1], cfg.sep_char)}\n"
            else:
                content = content + f"{1 + user + (15 * (page - 1))}. **{page_users[user][0]}** ⠂{uffx.QuantityToText(page_users[user][1], cfg.sep_char)}\n"

        if content != "":
            embed.add_field(name="", value=content, inline=False)

    return embed


class Leaderboard(discord.ui.View):
    def __init__(self, users:list, user_id:int, game:str, span:str, timeout=3600):
        super().__init__(timeout=timeout)
        self.total_pages = (len(users) // 15) + 1
        self.user_id = user_id
        self.page = 1
        self.lb = users
        self.game = game
        self.span = span

    #PREVIOUS
    @discord.ui.button(label="", emoji = "⬅️", style=discord.ButtonStyle.grey)
    async def Previous(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user.id != self.user_id:
            return

        if self.page > 1:
            self.page -= 1
        else:
            self.page = self.total_pages

        await interaction.response.edit_message(embed=PageEmbed(self.lb, self.page, self.game, self.span), view=self)


    #NEXT
    @discord.ui.button(label="", emoji = "➡️", style=discord.ButtonStyle.grey)
    async def Next(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user.id != self.user_id:
            return

        if self.page < self.total_pages:
            self.page += 1
        else:
            self.page = 1

        await interaction.response.edit_message(embed=PageEmbed(self.lb, self.page, self.game, self.span), view=self)


class LB(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="lb", description="Look at the leaderboards")
    @app_commands.guilds(discord.Object(id=cfg.guild_id))
    async def lb(self, interaction: discord.Interaction, game: Literal["Territorial", "OpenFront"], span: Literal["custom (in days)", "week", "day", "event", "alltime", "season"], days: app_commands.Range[int, 1, 60] | None):
        if ermg.UserExistCheck(interaction.user.id):
            gamedict = {"Territorial": "tt", "OpenFront": "of"}

            users = {}

            if span in ["event", "alltime", "season"]:
                for file in os.listdir(f"../{cfg.project_name}/users/"):

                    file_name = str(os.fsdecode(file))
                    user_data = dtmg.read_json(f"../{cfg.project_name}/users/{file_name}")

                    if user_data[gamedict[game]][f"{span}_pts"] > 0:
                        users[user_data["name"]] = user_data[gamedict[game]][f"{span}_pts"]
            
            else:
                now = time.time()

                if span == "day":
                    starting_time = now - 86400
                elif span ==  "week":
                    starting_time = now - 604800
                else:
                    starting_time = now - (days * 86400)

                starting_time = round(starting_time)
                
                for file in os.listdir(f"../{cfg.project_name}/users_log/"):
                    file_name = str(os.fsdecode(file))
                    user_data = dtmg.read_json(f"../{cfg.project_name}/users/{file_name[:-3]}json")

                    points = 0

                    with open(f"../{cfg.project_name}/users_log/{interaction.user.id}.txt", "r") as UFL:
                        for line in UFL.readlines():
                            log = line.split(",")

                            if int(log[0]) >= starting_time and log[1] == gamedict[game]:
                                points += int(log[2])

                    if points > 0:
                        users[user_data["name"]] = points

            if len(users) > 1:
                lb = sorted(users.items(), key=lambda user: user[1], reverse=True)
            else:
                lb = users
            
            if span != "custom (in days)":
                true_span = span
            else:
                true_span = str(days)
            
            await interaction.response.send_message(embed=PageEmbed(lb, 1, game, true_span), view=Leaderboard(lb, interaction.user.id, game, true_span))
        else:
            await interaction.response.send_message(embed=ermg.UserExistEmbed())

        
async def setup(bot) -> None:
    await bot.add_cog(LB(bot), override=True)