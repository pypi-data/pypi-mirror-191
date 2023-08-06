from email.errors import FirstHeaderLineIsContinuationDefect
import functools
from cetl.utils.builder import TEST_TRANSFORMERS, pd
from ..utils.base import Base
from cetl.utils.timer import timeit


@TEST_TRANSFORMERS.add()
class parallelTransformer(Base):
    def __init__(self, transformers: list):
        self.transformers = transformers

    @timeit
    def transform(self, dataframe)-> list:
        if isinstance(dataframe, list):
            dfs=dataframe
        elif isinstance(dataframe, pd.DataFrame):
            dfs = [dataframe]

        assert len(self.transformers)>0
        pipelines = []
        for i, transformer in enumerate(self.transformers):
            pipelines.append(transformer.transform(dfs[i]))

        return pipelines