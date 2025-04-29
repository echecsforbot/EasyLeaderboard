import json
import importlib
import time

ermg = importlib.import_module("tools.errors_manager")
dtmg = importlib.import_module("tools.data_manager")
cfg = importlib.import_module("tools.config")

def CreateUser(user, user_name):
        new_user = {
            "name": user_name,
            "of": {
                "season_pts": 0,
                "event_pts": 0,
                "alltime_pts": 0,
                "last_pts": 0
            },
            "tt": {
                "season_pts": 0,
                "event_pts": 0,
                "alltime_pts": 0,
                "last_pts": 0
            }
        }

        userjson = json.dumps(new_user, indent=3)
        with open(f"../{cfg.project_name}/users/{user.id}.json", "w", encoding = "utf-8") as UF:
            UF.write(userjson)

        now = round(time.time())
        with open(f"../{cfg.project_name}/users_log/{user.id}.txt", "w") as UFL:
            UFL.write(f"{now},of,0\n{now},tt,0")


def QuantityToText(quantity:int, char:str):
    text = ""
    end = ""

    negative = False
    if "-" in str(quantity):
        negative = True
        quantity = str(quantity)[1:]

    if "." in str(quantity):
        end = str(quantity)[str(quantity).find("."):]

    digit_passed = 0

    for digit in range(len(str(quantity)) - len(end) - 1, -1, -1):
        if digit_passed % 3 == 0 and digit_passed != 0:
            text = f"{char}" + text
        text = str(quantity)[digit] + text
        digit_passed += 1

    text = text + end

    if negative:
        text = "-" + text

    if text[-2:] == ".0":
        text = text[:-2]

    return text