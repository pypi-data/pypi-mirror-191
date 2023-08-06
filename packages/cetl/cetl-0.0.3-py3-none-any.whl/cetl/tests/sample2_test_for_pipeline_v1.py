import sys 
sys.path.append('.')
from cetl.utils.pipeline_v1 import DataPipeline


result=""
cfg = {"pipeline":[
                    {"type":"addRowNumber"},
                    {"type":"parallelTransformer", "isParallel":1, "transformers":[
                            {"type":"format2String", "description":"help following filterBy transformer"},
                            {"pipeline":[   {"type":"filterBy"},
                                            {"type":"parallelTransformer", "isParallel":1, "transformers":[
                                                {"type":"addRowNumber"},
                                                {"type":"passDataFrame"}]},
                                            {"type":"toCSV", "out_dir":"./", "out_file":"out.csv"}]},
                            {"pipeline":[{"type":"paddingZero"}]},
                            {"type":"dropColumns", "description":"remove temp columns"}
                        ]},
                    {"type":"passDataFrame"},
                    {"pipeline":[   {"type":"passDataFrame"},
                                    {"type":"toCSV", "out_dir":"./", "out_file":"out.csv"}]}
        ]}


pipe = DataPipeline(cfg)
# print(pipe._node_pairs)
# print(pipe._nodename2transformer)
pipe = pipe.create_dot_graph()
pipe.save_png("./sample1.2.png")
# print(pipe._dot)


# python3.6 cetl/tests/sample2.py