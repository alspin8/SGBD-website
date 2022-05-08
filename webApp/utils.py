import random, json, logging

def get_dict_from_jsonfile(file):
    with open(file) as json_data:
        data_json = json.load(json_data)
    data_str = json.dumps(data_json)
    return json.loads(data_str) 

class Logger:
    
    def __init__(self, level=logging.INFO) -> None:
        logging.basicConfig(filename = "../logs/logs.log",      
                            filemode = "a",
                            format = "%(levelname)s %(asctime)s - %(message)s",
                            level = level)
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(level)

    def get_logger(self): return self.__logger   