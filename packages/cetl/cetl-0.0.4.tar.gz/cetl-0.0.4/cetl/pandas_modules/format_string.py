from cetl.utils.builder import PANDAS_TRANSFORMERS, pd
from .base import Base

@PANDAS_TRANSFORMERS.add()
class format2String(Base):
    def __init__(self, base_fields=None):
        self.base_fields = base_fields


    def transform(self, dataframe)-> pd.DataFrame:
        df = dataframe
        for field in self.base_fields:
            df[field] = df[field].astype(str)
        return df
