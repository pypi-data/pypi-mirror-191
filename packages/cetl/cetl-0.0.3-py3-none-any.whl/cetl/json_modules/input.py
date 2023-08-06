from .base import Base
from cetl.utils.builder import TRANSFORMERS
import csv
import json

@TRANSFORMERS.add()
class readCSVAsJson(Base):
    def __init__(self,
                filepath=None , 
                delimiter=","):
        """
        the value of "keep" can be "last", False, "first"
        {"type":"readCSVAsJson", "filepath":"/home/clement/data/data_warehouse/Orders.csv", 
            "delimiter":","}
        """
        self.filepath = filepath
        self.delimiter=delimiter

    def transform(self, input_data):

        data = []
        with open(self.filepath, encoding='utf-8') as f:
            csvReader = csv.DictReader(f, delimiter=self.delimiter)
            # csvReader = csv.reader(f, delimiter=self.delimiter)
        
            # data = list(csvReader)
            for row in csvReader:
                data.append(row)

        json_str = json.dumps({"json_data":data}, indent=4)

        json_obj = json.loads(json_str)

        return json_obj