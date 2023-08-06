from ..utils.base import Base
from cetl.utils.builder import TEST_TRANSFORMERS, pd
import os
from cetl.utils.timer import timeit


@TEST_TRANSFORMERS.add()
class passDataFrame(Base):
    """do nothing"""
    def __init__(self, parallel_index=None):
        self.parallel_index=parallel_index

    @timeit
    def transform(self, dataframe)-> pd.DataFrame:
        if isinstance(dataframe, list):
            assert isinstance(self.parallel_index, int)
            return dataframe[self.parallel_index]
        elif isinstance(dataframe, pd.DataFrame):
            return dataframe

        return dataframe
