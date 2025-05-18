import toml


def game_data(file):
    with open(file, 'r') as f:
        data = toml.load(f)
    return data


def update_toml(new_data):
    try:
        with open('game_data.toml', 'r') as f:
            data = toml.load(f)
    except FileNotFoundError:
        data = {}

    data.update(new_data)

    with open('game_data.toml', 'w') as s:
        toml.dump(data, s)
