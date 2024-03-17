import pandas as pd







def DataFrameWrapper(required_columns: list[str]):
    class Wrapper:

        def __init__(self, *args, **kwargs):
            self.raw = pd.DataFrame(*args, **kwargs)
            if any(c not in self.raw.columns for c in required_columns):
                raise ValueError(
                    f'DataFrame non valido. \nColonne necessarie: {required_columns}\nColonne disponibili: {self.raw.columns}')
        def __repr__(self):
            return repr(self.raw)

    return Wrapper


