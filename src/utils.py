def round_json(data: dict):
    for key, value in data.items():
        if type(value) == list:
            for ind, el in enumerate(value):
                value[ind] = round_json(el)
            data[key] = value
        elif type(value) == dict:
            data[key] = round_json(value)
        elif type(value) == float:
            data[key] = round(value)
    return data



