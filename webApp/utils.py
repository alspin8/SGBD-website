import json

def get_dict_from_jsonfile(file):
    with open(file) as json_data:
        data_json = json.load(json_data)
    data_str = json.dumps(data_json)
    return json.loads(data_str) 