from .base import Base
from cetl.utils.builder import PANDAS_TRANSFORMERS, pd

@PANDAS_TRANSFORMERS.add()
class filterBy(Base):
    def __init__(self, fieldname=None, fieldvalue=None, Op="true", parallel_index=None):
        self.fieldname = fieldname
        self.fieldvalue = fieldvalue
        self.Op = Op
        self.parallel_index=parallel_index

    def transform(self, dataframe)  -> pd.DataFrame:
        if isinstance(dataframe, list):
            assert isinstance(self.parallel_index, int)
            df=dataframe[self.parallel_index]
        elif isinstance(dataframe, pd.DataFrame):
            df = dataframe
        else:
            print("input should be pandas DataFrame or list of pandas DataFrames")

        if self.Op=="true":
            df = df[df[self.fieldname]==self.fieldvalue]
        elif self.Op=="false":
            df = df[df[self.fieldname]!=self.fieldvalue]
        return df