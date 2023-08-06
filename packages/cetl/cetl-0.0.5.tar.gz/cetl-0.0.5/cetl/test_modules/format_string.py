from cetl.utils.builder import TEST_TRANSFORMERS, pd
from ..utils.base import Base
from cetl.utils.timer import timeit

@TEST_TRANSFORMERS.add()
class format2String(Base):
    def __init__(self, base_fields=None):
        self.base_fields = base_fields

    @timeit
    def transform(self, dataframe)-> pd.DataFrame:
        df = dataframe
        for field in self.base_fields:
            df[field] = df[field].astype(str)
        return df
