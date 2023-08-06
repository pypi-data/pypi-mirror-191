import sys 
sys.path.append('.')
from cetl.utils.pipeline_v1 import DataPipeline


result=""
cfg = {"pipeline":[
                    {"type":"addRowNumber"},
                    {"type":"parallelTransformer", "isParallel":1, "transformers":[
                            {"type":"format2String", "description":"help following filterBy transformer"},
                            {"pipeline":[{"type":"filterBy"}]},
                            {"pipeline":[{"type":"paddingZero"}]},
                            {"type":"dropColumns"}
                        ]},
                    {"type":"passDataFrame"},
                    {"pipeline":[   {"type":"passDataFrame"},
                                    {"type":"toCSV", "out_dir":"./", "out_file":"out.csv"}]}
        ]}


pipe = DataPipeline(cfg)
print(pipe._node_pairs)
pipe = pipe.create_dot_graph()
# python3.6 cetl/tests/sample1.py
pipe.save_png("./sample1.1.png")
# print(pipe._dot)