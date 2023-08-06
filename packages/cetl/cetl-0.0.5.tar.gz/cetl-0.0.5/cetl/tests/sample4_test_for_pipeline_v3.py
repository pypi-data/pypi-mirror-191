import sys 
sys.path.append('.')
from cetl import DataPipeline
from cetl.utils.builder import TRANSFORMERS


result=""
cfg = {"pipeline":[{"type":"readCSVAsJson", 
                        "filepath":"/home/clement/data/for_json_pipeline/Orders.csv", 
                        "delimiter":"\t"},
                    {"type":"dropColumns", "subset":["EmployeeID", "ShipperID"]}
        ]}


pipe = DataPipeline(cfg)
print(pipe.steps)
# result=pipe.transform(result)

print(result)

# python3.6 cetl/tests/sample4_test_for_pipeline_v3.py