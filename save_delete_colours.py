import json
import os.path

FILE = "saved_colours.json"


def save_to_json(index: int, rgb: tuple, hsl: tuple, hex_value: str):
    """Save colour hex to a json file"""
    new_data = {
        index: {
            "rgb": rgb,
            "hsl": hsl,
            "hex": hex_value
        }
    }

    if os.path.exists(FILE):
        if os.path.getsize(FILE) == 0:
            with open(FILE, mode="a") as file_path:
                json.dump(new_data, file_path, indent=4)
        else:
            with open(FILE, mode="r") as file_path:
                data = json.load(file_path)
                data.update(new_data)
                with open(FILE, mode="w") as new_file_path:
                    json.dump(data, new_file_path, indent=4)
    else:
        with open(FILE, mode="w") as file_path:
            json.dump(new_data, file_path, indent=4)


def delete_from_json(index: int):
    """deletes saved colour hex stored in the created
    json file"""
    if os.path.exists(FILE):
        with open(FILE, mode="r") as file_path:
            data = json.load(file_path)
            data.pop(str(index))
            data.update(data)
            with open(FILE, mode="w") as new_file_path:
                json.dump(data, new_file_path, indent=4)


def preload_from_json() -> tuple:
    """returns a tuple of two list, the tuple
    includes a list of keys and a list of values"""
    list_to_return = []
    indexes = []
    if os.path.exists(FILE):
        if os.path.getsize(FILE) == 0:
            return indexes, list_to_return
        with open(FILE, mode="r") as file_path:
            data = json.load(file_path)
            for i, j in data.items():
                indexes.append(int(i))
                list_to_return.append(j)
    return indexes, list_to_return
