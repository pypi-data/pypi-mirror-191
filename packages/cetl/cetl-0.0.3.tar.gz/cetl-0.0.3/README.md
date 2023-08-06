python requirement = 3.6.3


# build pypi packages
```sh
# go to the root folder
python3 setup.py sdist bdist_wheel
```

# install cetl from dist folder
```sh
python3.6 -m pip install dist/cetl-0.0.3.tar.gz
```

# upload the built package to test pypi
```
twine upload --repository testpypi dist/*
username: clement_cheuk-.43
```


# upload to offical pypi
```
twine upload dist/*
```

import pydot

dot_string = """graph my_graph {
    bgcolor="yellow";
    a [label="Foo"];
    b [shape=circle];
    a -- b -- c [color=blue];
}"""

graphs = pydot.graph_from_dot_data(dot_string)
graph = graphs[0]
graph.write_svg('big_data.svg')


# developing tests
```sh
cd cetl
python3.6 cetl/tests/sample2.py
```