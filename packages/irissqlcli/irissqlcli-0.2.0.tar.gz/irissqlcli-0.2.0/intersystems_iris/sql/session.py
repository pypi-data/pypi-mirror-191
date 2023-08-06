import pandas
from sqlalchemy import create_engine
from .dataframe import DataFrame

class IRISSession:
    default_schema = 'SQLUser'

    def __init__(self) -> None:
        self.engine = create_engine('iris+emb:///')
    
    def table(self, full_name) -> DataFrame:
        [schema, table] = full_name.split('.') if '.' in full_name else [self.default_schema, full_name]
        df = pandas.read_sql_table(table, self.engine, schema=schema)
        return DataFrame(df)
