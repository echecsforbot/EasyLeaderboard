import json
import importlib

cfg = importlib.import_module("tools.config")

def read_json(file_path:str):
    with open(file_path, "r", encoding = "utf-8") as UF:
        return json.load(UF)
      

def write_new_data(newdata:dict, user_id:int):
    newdata_content = json.dumps(newdata, indent=3)
    with open(f"../{cfg.project_name}/users/{user_id}.json", "w", encoding = "utf-8") as UF:
        UF.write(newdata_content)


def UpdateUserData(user_data:dict, operation_type:str, new_value, layers:list):
    if len(layers) == 1:
        if operation_type == "set":
            user_data[layers[0]] = new_value

        elif operation_type == "add":
            if layers[0] in user_data.keys():
                user_data[layers[0]] += new_value
                user_data[layers[0]] = int(user_data[layers[0]])
            else:
                user_data[layers[0]] = new_value 

    else:
        layer = layers[0]

        if layer in user_data.keys():
            UpdateUserData(user_data[layer], operation_type, new_value, layers[1:])


def ChangeData(user_id:int, operation_type:str, new_value, *layers:str):
    ufd = read_json(f"../{cfg.project_name}/users/{user_id}.json")

    UpdateUserData(ufd, operation_type, new_value, layers)

    write_new_data(ufd, user_id)