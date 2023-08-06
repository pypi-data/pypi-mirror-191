from cetl.utils.builder import TEST_TRANSFORMERS, pd
from ..utils.base import Base
from cetl.utils.timer import timeit
import os


@TEST_TRANSFORMERS.add()
class toCSV(Base):
    def __init__(self, out_dir=None, out_file=None, parallel_index=None, delimiter="|"):
        self.out_dir = out_dir
        self.out_file = os.path.join(out_dir, out_file)
        self.parallel_index=parallel_index
        self.delimiter=delimiter

    @timeit
    def transform(self, dataframe)-> pd.DataFrame:
        if isinstance(dataframe, list):
            assert isinstance(self.parallel_index, int)
            df=dataframe[self.parallel_index]
        elif isinstance(dataframe, pd.DataFrame):
            df = dataframe

        #create dir
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

        df.to_csv(self.out_file, index=None, sep=self.delimiter)

        return df
