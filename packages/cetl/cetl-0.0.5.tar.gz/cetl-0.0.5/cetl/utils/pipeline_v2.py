from sklearn.pipeline import Pipeline as sklearn_pipeline
from collections import defaultdict
import copy
import graphviz
from flask import send_file
import tempfile
import os
import inspect
import re
from cetl.utils.builder import PANDAS_TRANSFORMERS, JSON_TRANSFORMERS, SPARK_TRANSFORMERS

def get_register(data_container_type):
    TRANSFORMERS=None
    # data_container_type is like "pandas", "json" or "spark"
    if data_container_type=="pandas":
        TRANSFORMERS = PANDAS_TRANSFORMERS
    elif data_container_type=="json":
        TRANSFORMERS = JSON_TRANSFORMERS
    elif data_container_type=="spark":
        TRANSFORMERS = SPARK_TRANSFORMERS
    elif data_container_type=="":
        TRANSFORMERS = PANDAS_TRANSFORMERS
    else:
        raise ValueError(f"data_container_type, {data_container_type} is not recognized by cetl")

    return TRANSFORMERS

# when build_pipeline, it will return Pipeline
class Pipeline(sklearn_pipeline):
    def __init__(self, 
                 steps, 
                 *, 
                 memory=None,
                 verbose=False,
                 pipe_start=1,
                 pipe_stop=None):
        
        self.steps = steps
        self.memory = memory
        self.verbose = verbose
        self.pipe_start = pipe_start
        self.pipe_stop = pipe_stop
        
    
    def _islice(self, target_list, start, end):
        total = len(target_list)
        assert end <=total, "end is higher total elements"
        
        selected_elements=None
        
        if start>0 and end ==-1:
            selected_elements = target_list[start-1:]
        elif start<0 and end==-1:
            selected_elements = target_list[start:]
        elif start>0 and end >0:
            selected_elements = target_list[start-1:end]
        elif start<0 and end <0:
            selected_elements = target_list[start:end+1]
        elif start>0 and end <0:
            selected_elements = target_list[start-1:end+1]
            
        return selected_elements

    
    def _iter(self):
        print("running _iter #########################")
        if self.pipe_stop ==None:
            self.pipe_stop = len(self.steps)
        for idx, (name, trans) in enumerate(self._islice(self.steps, self.pipe_start, self.pipe_stop)):
            yield idx, name, trans
        
        
    def select_transformers(self, pipe_start=None, pipe_stop=None):
        self.pipe_start = pipe_start
        self.pipe_stop = pipe_stop
        new = copy.deepcopy(self)
        
        new.steps = self._islice(self.steps, self.pipe_start, self.pipe_stop)
        
        return new
    

def _name_estimators(estimators):
    """Generate names for estimators."""

    names = [
        estimator if isinstance(estimator, str) else type(estimator).__name__.lower()
        for estimator in estimators
    ]
    namecount = defaultdict(int)
    for est, name in zip(estimators, names):
        namecount[name] += 1

    for k, v in list(namecount.items()):
        if v == 1:
            del namecount[k]

    for i in reversed(range(len(estimators))):
        name = names[i]
        if name in namecount:
            names[i] += "-%d" % namecount[name]
            namecount[name] -= 1

    return list(zip(names, estimators))
        
def make_pipeline(*steps, memory=None, verbose=False):
    """
    Examples
    -----------
    >>> from core.utils.pipeline import build_pipeline
    >>> build_pipeline(addNewColumn(), drop_columns())
    Pipeline(transformers=[ 'addNewColumn', addNewColumn(),
                            'drop_columns', drop_columns()])
    """
    # print(steps)
    return Pipeline(_name_estimators(steps), memory=memory, verbose=verbose)

def build_transformer_from_cfg(cfg, registry, parallel_transformers=None):
    args = cfg.copy()
    transformer_type = args.pop("type")
    
    cls_obj = registry.module_dict[transformer_type]
    
    transformer=None
    if transformer_type=="parallelTransformer":
        transformer = cls_obj(parallel_transformers)
        
    else:
        transformer = cls_obj(**args)

    return transformer  

def create_tranformers_dict(transformers):
    id2transformer = {}
    nodename2transformer = {}
    for transformer in transformers:
        id2transformer[transformer.index] = transformer
        nodename2transformer[transformer.node_name] = transformer

    return id2transformer, nodename2transformer


display_parallel = False
display_sub_pipeline = True
def update_node(current_node=None, new_node=None):
    return current_node, new_node



def recursive_build_pipeline_from_cfg(cfg, simple_node_pairs, node_pairs, latest_node, index, parallel_index, nodename2transformer):
    """
    Examples
    -----------
    global_index = 0
    latest_node = ""
    node_pairs = []

    pipeline, node_pairs, latest_node, index = recursive_build_pipeline_from_cfg(cfg, node_pairs, latest_node, global_index)
    """

    assert "pipeline" in cfg
    
    steps = []

    for trans_cfg in cfg["pipeline"]:
        trans_name = trans_cfg.get("type")  if "type" in trans_cfg else ""
        trans_name = "pipeline" if "pipeline" in trans_cfg else trans_name

        
        if trans_name == "parallelTransformer":         
            
            
            ########################## adding intermediate node for parallelTransformer
            parallel_name = "parallel"
            parallel_index +=1
            default_parallel_label = "parallelTransformer"
            parallel_node_name = f"{parallel_name} #{parallel_index}"
            
            if display_parallel:
                previous_node, latest_node = update_node(latest_node, parallel_node_name)
                if isinstance(previous_node, str):
                    simple_node_pairs.append((previous_node, latest_node, default_parallel_label))
                    node_pairs.append((previous_node, latest_node, default_parallel_label))
                elif isinstance(previous_node, list):
                    for _previous_node in previous_node:
                        simple_node_pairs.append((_previous_node, latest_node, default_parallel_label))
                        node_pairs.append((_previous_node, latest_node, default_parallel_label))
                else:
                    assert False, "latest_node is not str or list"
            ######################### END


            transformers_list = []
            parallel_latest_node = []
            parallel_node_pairs = {}
            latest_nodes = None
            if isinstance(latest_node,str):
                #convert the _previous_node to a list
                latest_nodes= [latest_node for i in range(len(trans_cfg["transformers"]))]
            elif isinstance(latest_node, list):
                latest_nodes = latest_node
            else:
                assert False, "latest_node is not str or list"

            parallel_dict_index = [i for i in range(len(latest_node))]
            for i, latest_node, sub_trans_cfg in zip(parallel_dict_index, latest_nodes, trans_cfg["transformers"]):
                
                if "type" in sub_trans_cfg:
                    sub_trans_name = sub_trans_cfg.get("type")
                    ############################### dealling with previous transformer is also parallelTransformer
                    assert sub_trans_name!="parallelTransformer", "parallel is not acceptable in parallelTransfomer"
                    ######################### END

                    #add note pair
                    index = index + 1
                    description = sub_trans_cfg.pop("description") if "description" in sub_trans_cfg else ""
                    data_container_type = trans_cfg.pop("data_container_type") if "data_container_type" in trans_cfg else ""
                    TRANSFORMERS = get_register(data_container_type)
                    transformer = build_transformer_from_cfg(sub_trans_cfg, TRANSFORMERS)
                    transformer.index = index
                    transformer.node_name = f"{str(index)}.{sub_trans_name}"
                    transformer.description = description
                    transformers_list.append(transformer)
                    # update nodename2transformer
                    nodename2transformer[transformer.node_name] = transformer
                    # update steps list
                    previous_node, _latest_node = update_node(latest_node, transformer.node_name)
                    parallel_node_pairs[f"process #{str(i)}"]=(previous_node, _latest_node)
                    simple_node_pairs.append((previous_node, _latest_node))
                    parallel_latest_node.append(_latest_node)


                elif "pipeline" in sub_trans_cfg:
                    transformer, simple_node_pairs, _node_pairs, _latest_node, index, parallel_index, nodename2transformer = recursive_build_pipeline_from_cfg(sub_trans_cfg, 
                                                                                                                                                                simple_node_pairs, 
                                                                                                                                                                [], 
                                                                                                                                                                latest_node, 
                                                                                                                                                                index, 
                                                                                                                                                                parallel_index, 
                                                                                                                                                                nodename2transformer)
                    transformers_list.append(transformer)
                    parallel_node_pairs[f"process #{str(i)}"]=_node_pairs
                    parallel_latest_node.append(_latest_node)


            # updaet latest_node                                                
            previous_node, latest_node = update_node(latest_nodes, parallel_latest_node)
            # update node_pairs
            node_pairs.append(parallel_node_pairs)
            # add steps
            data_container_type = trans_cfg.pop("data_container_type") if "data_container_type" in trans_cfg else ""
            TRANSFORMERS = get_register(data_container_type)
            parallel_transformer = build_transformer_from_cfg(trans_cfg, 
                                                              TRANSFORMERS, 
                                                              transformers_list)
            steps.append(parallel_transformer)
            # update nodename2transformer
            nodename2transformer[parallel_node_name] = parallel_transformer


            
        elif trans_name=="pipeline":
            # recursive function help update node_pairs, latest_node and index
            _pipeline, simple_node_pairs, _node_pairs, latest_node, index, parallel_index, nodename2transformer= recursive_build_pipeline_from_cfg(trans_cfg, 
                                                                                                                                                    simple_node_pairs, 
                                                                                                                                                    [], 
                                                                                                                                                    latest_node, 
                                                                                                                                                    index, 
                                                                                                                                                    parallel_index, 
                                                                                                                                                    nodename2transformer)
            # update steps
            node_pairs.append(_node_pairs)
            steps.append(_pipeline)
        
        else:
            index = index + 1
            node_name = f"{str(index)}.{trans_name}"
            description = trans_cfg.pop("description") if "description" in trans_cfg else ""
            data_container_type = trans_cfg.pop("data_container_type") if "data_container_type" in trans_cfg else ""
            TRANSFORMERS = get_register(data_container_type)
            transformer = build_transformer_from_cfg(trans_cfg, TRANSFORMERS)
            transformer.index = index
            transformer.node_name = node_name
            transformer.description = description
            
            # update steps list
            steps.append(transformer)
            # update nodename2transformer
            nodename2transformer[node_name] = transformer
            # update node_pairs
            if isinstance(latest_node, str):
                simple_node_pairs.append((latest_node, node_name))
                node_pairs.append((latest_node, node_name))
            elif isinstance(latest_node, list):
                for item in latest_node:
                    simple_node_pairs.append((item, node_name))
                    node_pairs.append((item, node_name))
            #update latest_node
            latest_node = node_name

    # remove empty node in node pair
    simple_node_pairs = [item for item in simple_node_pairs if item[0]!=""]

    return make_pipeline(*steps), simple_node_pairs, node_pairs, latest_node, index, parallel_index, nodename2transformer
            

def recursive_create_dot_graph(_predot, _dot, node_pairs, parallel_index, pipeline_index):
    """
    shape reference: https://graphviz.org/doc/info/shapes.html

    format for node_pairs:
    with display_parallel=True
    --------------------
    [   ('', '1.addRowNumber'), 
        ('1.addRowNumber', 'parallel #1', 'parallelTransformer'), 
        {   'process #0': ('parallel #1', '2.format2String'), 
            'process #1': [ ('parallel #1', '3.filterBy'), 
                            ('3.filterBy', 'parallel #2', 'parallelTransformer'), 
                            {   'process #0': ('parallel #2', '4.addRowNumber'), 
                                'process #1': ('parallel #2', '5.passDataFrame')}, 
                            ('4.addRowNumber', '6.toCSV'), 
                            ('5.passDataFrame', '6.toCSV')], 
            'process #2': [('parallel #1', '7.paddingZero')], 
            'process #3': ('parallel #1', '8.dropColumns')}, 
                            ('2.format2String', '9.passDataFrame'), 
                            ('6.toCSV', '9.passDataFrame'), 
                            ('7.paddingZero', '9.passDataFrame'), 
                            ('8.dropColumns', '9.passDataFrame'), 
                            [('9.passDataFrame', '10.passDataFrame'), ('10.passDataFrame', '11.toCSV')]]
    
    with display_parallel=False
    --------------------
    [('', '1.addRowNumber'), 
        {   'process #0': ('1.addRowNumber', '2.format2String'), 
            'process #1': [('1.addRowNumber', '3.filterBy'), {'process #0': ('3.filterBy', '4.addRowNumber'), 
                                                            'process #1': ('3.filterBy', '5.passDataFrame')}, 
                                                            ('4.addRowNumber', '6.toCSV'), ('5.passDataFrame', '6.toCSV')], 
            'process #2': [('1.addRowNumber', '7.paddingZero')], 
            'process #3': ('1.addRowNumber', '8.dropColumns')}, 
        ('2.format2String', '9.passDataFrame'), 
        ('6.toCSV', '9.passDataFrame'), 
        ('7.paddingZero', '9.passDataFrame'), 
        ('8.dropColumns', '9.passDataFrame'), 
        [('9.passDataFrame', '10.passDataFrame'), ('10.passDataFrame', '11.toCSV')]]

    """
    
    for i, sub_node_pairs in enumerate(node_pairs):
        if isinstance(sub_node_pairs, dict):
            num_parallel_pairs = len(sub_node_pairs)
            # make parallelTransformer cluster
            if display_parallel:
                parallel_index = parallel_index + 1 if num_parallel_pairs>1 else parallel_index
                _sub_dot = _dot.subgraph(name=f"cluster_{str(parallel_index)}")
                _sub_dot.attr(label=f"parallel cluster #{str(parallel_index)}", color="blue")
            else:
                _sub_dot = _dot
            
            for j, sub_node_pair in enumerate(sub_node_pairs.values()):
                
                if isinstance(sub_node_pair, tuple):
                    
                    _usage_dot_ = _sub_dot  if j!=0 else _dot
                    if sub_node_pair[0]!="":
                        _usage_dot_.edge(sub_node_pair[0], sub_node_pair[1], label="")

                elif isinstance(sub_node_pair, list):
                    
                    if display_sub_pipeline:
                        num_sub_pipeline_pairs = len(sub_node_pair)
                        pipeline_index = pipeline_index + 1 if num_sub_pipeline_pairs>1 else pipeline_index
                        with _sub_dot.subgraph(name=f"cluster_{str(pipeline_index)}") as _sub_pipeline_dot:
                            _sub_pipeline_dot.attr(label=f"pipeline cluster #{str(pipeline_index)}", color="blue")
                            _, _, parallel_index, pipeline_index = recursive_create_dot_graph(_sub_dot, _sub_pipeline_dot, sub_node_pair, parallel_index, pipeline_index)
                    else:
                        _sub_pipeline_dot = _sub_dot
                        _, _, parallel_index, pipeline_index = recursive_create_dot_graph(_sub_dot, _sub_pipeline_dot, sub_node_pair, parallel_index, pipeline_index)

        elif isinstance(sub_node_pairs, list):
            num_pipeline_pairs = len(sub_node_pairs)
            # make pipeline cluster
            if display_sub_pipeline:
                pipeline_index = pipeline_index + 1 if num_pipeline_pairs> 1 else pipeline_index
                with _dot.subgraph(name=f"cluster_{str(pipeline_index)}") as c:
                    c.attr(label=f"pipeline cluster #{str(pipeline_index)}", color="blue")
                    _, _, parallel_index, pipeline_index = recursive_create_dot_graph(_dot, c, sub_node_pairs, parallel_index, pipeline_index)
            else:
                # if display_pipeline is False, do not use subgraph
                _, _, parallel_index, pipeline_index = recursive_create_dot_graph(_dot, _dot, sub_node_pairs, parallel_index, pipeline_index)

        elif isinstance(sub_node_pairs, tuple):
            _usage_dot_ = _dot if i!=0 else _predot
            # make transformer edge
            node_pair = sub_node_pairs
            if node_pair[0]!="":
                _usage_dot_.edge(node_pair[0], node_pair[1], label="") 
                if len(node_pair)>2:
                    if node_pair[2]=="parallelTransformer":
                        _usage_dot_.node(node_pair[1], shape='Msquare')
                else:
                    pass
                    # _dot.node(node_pair[0], shape='rect')
                    # _dot.node(node_pair[1], shape='rect')

    return _predot, _dot, parallel_index, pipeline_index

class DataPipeline:
    """
    usage
    --------------
    pipe = DataPipeline(cfg)
    pipe.transformer()
    """
    def __init__(self, cfg):
        self._cfg = cfg
        self._simple_node_pairs=[]
        self._node_pairs = []
        self._latest_node = ""
        self._index = 0
        self._parallel_index=0
        self._dot = None
        self._nodename2transformer={}
        self._pipeline = self.build_pipeline_from_cfg()
        self.steps = self._pipeline.steps


    def build_pipeline_from_cfg(self):
        _pipeline, self._simple_node_pairs, self._node_pairs, self._latest_node, index, parallel_index, self._nodename2transformer= recursive_build_pipeline_from_cfg(self._cfg, 
                                                                                                                                                                self._simple_node_pairs,
                                                                                                                                                                self._node_pairs, 
                                                                                                                                                                self._latest_node, 
                                                                                                                                                                self._index,
                                                                                                                                                                self._parallel_index,
                                                                                                                                                                self._nodename2transformer)
        return _pipeline

    def create_simple_dot_graph(self):
        """
        Tutorial: https://graphviz.readthedocs.io/en/stable/examples.html
        """
        self._dot = graphviz.Graph("pipeline graph", format='png')
        # general styel
        self._dot.attr('node', 
                        shape="rect", 
                        style="filled", 
                        fillcolor="skyblue4", 
                        color="white", 
                        fontcolor="white")
        self._dot.attr('edge',
                        arrowhead="normal",
                        arrowsize='1.0')
        # self._dot.graph_attr.update(directed="true")
        # self._dot.edge_attr(("directed","true"))
        

        # add node
        transformers_list=[]
        for item in self._simple_node_pairs:
            transformers_list = transformers_list + list(item)
        transformers_set = sorted(set(transformers_list))
        for item in transformers_set:
            # add node
            self._dot.node(item, item+"\n")

        # # add edges
        for item in self._simple_node_pairs:
            # add edge
            self._dot.edge(item[0], item[1], 
                            label="")
        return self._dot

    def generate_node_text(self, 
                            node_name, 
                            description, 
                            inputs, 
                            output):
        limit = 25
        sep_line = "".join(["-" for i in range(limit)])

        ####################### description
        if len(description)>limit:
            description = description[:limit]+"..."
        if description:
            description = f"Description: {description}\l"

        ####################### input
        input_text=""
        for input in inputs:
            # print(input, len(input))
            if len(input)>limit:
                input_text += "        " + input[:limit]+"...\l"
            else:
                input_text += "        " + input+"\l"
        #https://www.digitalocean.com/community/tutorials/python-trim-string-rstrip-lstrip-strip
        input_text = input_text.lstrip()[:-2] if input_text else input_text

        ####################### output
        if len(output)>limit:
            output = output[:limit]+"..."

        node_text = f"{node_name}\l{sep_line}{sep_line}\l{description}Input: {input_text}\lOutput: {output}\l"
        # print(node_text)

        return node_text

    def create_dot_graph(self):
        """
        Tutorial: https://graphviz.readthedocs.io/en/stable/examples.html
        Note: graphviz.Graph have no direction, so no arrowhead
        """

        self._dot = graphviz.Digraph("pipeline graph", format='png')
        self._dot.attr('node', 
                        shape="rect", 
                        style="filled", 
                        fillcolor="skyblue4", 
                        color="white", 
                        fontcolor="white")

        # create nodes
        transformers_list=[]
        for item in self._simple_node_pairs:
            transformers_list = transformers_list + list(item)
        transformers_set = sorted(set(transformers_list))
        for item in transformers_set:
            if "parallelTransformer" in item:
                pass
            elif "parallel" in item:
                    self._dot.node(item)
            else:
                transformer = self._nodename2transformer[item]
                # get transformer description
                description = transformer.description
                #get the arguments of transformer.transform() as input
                inputs = [item for item in inspect.getfullargspec(transformer.transform).args if item not in ["self"]]
                # get the return value type
                # https://stackoverflow.com/questions/49560974/inspect-params-and-return-types
                output = str(inspect.signature(transformer.transform).return_annotation)
                # "<class 'int'>" extract the 'int'
                output = re.findall("\<class '+(.*?)\'>",output)
                output = output[0].split(".")[-1] if output else ""
                node_text = self.generate_node_text(item, description, inputs, output)
                self._dot.node(item, node_text)
            
            

        # create edges
        self._pre_dot, self._dot, parallel_index, pipeline_index = recursive_create_dot_graph(self._dot, self._dot, self._node_pairs, 0, 0)

        # add node

        return self



    def save_png(self, out_file):
        if out_file:
            ext = "." + out_file.split(".")[-1]
            out_file = out_file.replace(ext, "")
            print(out_file)
            self._dot.render(out_file).replace("\\", "/")
    

    def output_graph(self):
        with tempfile.NamedTemporaryFile(suffix=".png") as f:
            # print(f.name)
            dirname = os.path.dirname(f.name)
            base_name = os.path.basename(f.name)
            filename = base_name.replace(".png", "")
            self._dot.render(os.path.join(dirname, filename)).replace("\\", "/")
            return f.name
        
        return ""

    def send_api_graph(self):
        with tempfile.NamedTemporaryFile(suffix=".png") as f:
            # print(f.name)
            dirname = os.path.dirname(f.name)
            base_name = os.path.basename(f.name)
            filename = base_name.replace(".png", "")
            self._dot.render(os.path.join(dirname, filename)).replace("\\", "/")
            return send_file(f.name, as_attachment=True, attachment_filename=base_name)

    def transform(self, input):
        return self._pipeline.transform(input)