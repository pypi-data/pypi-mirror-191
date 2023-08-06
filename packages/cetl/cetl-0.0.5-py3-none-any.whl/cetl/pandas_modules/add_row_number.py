from .base import Base
from cetl.utils.builder import PANDAS_TRANSFORMERS, pd

@PANDAS_TRANSFORMERS.add()
class addRowNumber(Base):
    def __init__(self, mark_field="Number"):
        self.mark_field=mark_field

    def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        df = dataframe
        df['A'] = "A"
        df[self.mark_field] = df.groupby(['A']).cumcount()+1
        df=df.drop(columns=['A'])
        return df