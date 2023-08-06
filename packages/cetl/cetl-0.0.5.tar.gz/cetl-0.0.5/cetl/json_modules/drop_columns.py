from cetl.utils.base import Base
from cetl.utils.builder import JSON_TRANSFORMERS
from cetl.utils.timer import timeit

@JSON_TRANSFORMERS.add()
class dropColumns(Base):
    """
    {"type":"dropColumns", "subset":["EmployeeID"]}
    """
    def __init__(self, subset=None):
        self.subset = subset

    @timeit
    def transform(self, input_data:dict):
        for record in input_data["json_data"]:
            for field in self.subset:
                if field in record:
                    record.pop(field)
                else:
                    print(f"field {field} not exists")

        return input_data
