import sys 
sys.path.append('.')
from cetl import DataPipeline



result=""
cfg = {"pipeline":[{"type":"readCSV", "data_container_type":"json",
                        "filepath":"/home/clement/data/for_json_pipeline/Orders.csv", 
                        "delimiter":"\t"},
                    {"type":"dropColumns", "data_container_type":"json", "subset":["EmployeeID", "ShipperID"]}
        ]}


pipe = DataPipeline(cfg)
for step in pipe.steps:
    print(type(step[1]))

pipe = pipe.create_dot_graph()
pipe.save_png("./sample5.png")


# python3.6 cetl/tests/sample5_data_container_type.py