import json

def create_input(vote_value):
    data = {"vote": vote_value}
    with open("inputs.json", "w") as f:
        json.dump(data, f)

# Пример вызова:
create_input(1)
