from pandas import DataFrame as PandasDataFrame

class DataFrame:
    df = None
    
    def __init__(self, df: PandasDataFrame) -> None:
        self.df = df

    def limit(self, num: int) -> "DataFrame":
        return self