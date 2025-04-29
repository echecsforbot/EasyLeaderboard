import discord
import os
import importlib

dtmg = importlib.import_module("tools.data_manager")
uffx = importlib.import_module("tools.usefull_fx")
cfg = importlib.import_module("tools.config")

def UserExistCheck(user_id:int):
    for file_name in os.listdir(f"../{cfg.project_name}/users/"):
        if str(user_id) in file_name:
            return True
    return False
    
def ValidNameCheck(name:str):
    if len(name) < 3 or len(name) > 20:
        return False
    
    for char in range(len(name)):
        if name[char] in ["'", '"']:
            return False
        
    return True

def ValidNameEmbed():
    embed = discord.Embed(color=cfg.fail_color)
    embed.add_field(name="Invalid name", value="*Your name must be between 3 and 20 characters long and can't contain quotes and doubled quotes.*")
    return embed

def UserExistEmbed():
    embed = discord.Embed(color=cfg.fail_color)
    embed.add_field(name="I can't find you in the database...", value="*Use `/signin` to register and start adding your wins!*", inline=False)
    return embed

def AccountExistEmbed():
    embed = discord.Embed(color=cfg.fail_color)
    embed.add_field(name="You are already registered!", value="")
    return embed