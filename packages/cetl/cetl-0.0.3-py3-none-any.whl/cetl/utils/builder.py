from .registry import Registry
import pandas as pd
# pd.set_option('display.max_columns', None)

TRANSFORMERS = Registry("transformers")
DB_MAPPERS = Registry("src_db_mappers")
# tenant388_transaction_models =Registry("tenant388_transaction models")
# TB_MODELS = {"tenant388_transaction":tenant388_transaction_models}
DB_MODELS = Registry("db models")