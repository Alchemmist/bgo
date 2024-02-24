from typing import Any


def round_json(data: dict[str, Any]) -> dict[str, Any]:
    for key, value in data.items():
        if type(value) is list:
            for ind, el in enumerate(value):
                value[ind] = round_json(el)
            data[key] = value
        elif type(value) is dict:
            data[key] = round_json(value)
        elif type(value) is float:
            data[key] = round(int(value))
    return data
