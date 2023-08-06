from .base import Base
from cetl.utils.builder import PANDAS_TRANSFORMERS, pd

@PANDAS_TRANSFORMERS.add()
class dropColumns(Base):
    def __init__(self, subset=None, parallel_index=None):
        self.subset = subset
        self.parallel_index = parallel_index

    def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        if isinstance(dataframe, list):
            assert isinstance(self.parallel_index, int)
            df=dataframe[self.parallel_index]
        elif isinstance(dataframe, pd.DataFrame):
            df = dataframe

        #check the valid of field
        headers=list(df.columns)
        
        valid_fields = []
        for field in self.subset:
            if field in headers:
                valid_fields.append(field)
            else:
                print("field, {0} not exists in the dataframe".format(field))
        
        df = df.drop(columns=valid_fields)
        return df