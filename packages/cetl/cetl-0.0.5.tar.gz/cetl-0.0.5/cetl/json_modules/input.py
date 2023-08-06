from cetl.utils.base import Base
from cetl.utils.builder import JSON_TRANSFORMERS
from cetl.utils.timer import timeit
import csv
import json

@JSON_TRANSFORMERS.add()
class readCSV(Base):
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

    @timeit
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