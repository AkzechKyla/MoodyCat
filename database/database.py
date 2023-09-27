import json


async def import_data(user_id, action, points):
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    user_id = str(user_id)

    if user_id not in data:
        data[user_id] = {"total_score": 100, "actions": {}}

    data[user_id]["actions"][action] = points

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)


async def read_actions(user_id):
    with open("data.json", "r") as file:
        data = json.load(file)

    user_id = str(user_id)

    user_data = data.get(user_id, {})
    total_score = user_data.get("total_score", 0)
    actions = user_data.get("actions", {})

    return total_score, actions
