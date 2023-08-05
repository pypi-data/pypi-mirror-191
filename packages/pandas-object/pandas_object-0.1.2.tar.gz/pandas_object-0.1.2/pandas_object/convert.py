from pandas import DataFrame
from rich.console import Console
from rich.table import Table

console = Console(tab_size=4)


class PandasObjectRow:

    def __init__(
        self,
        df: DataFrame,
        row_index: int,
    ):
        self.df = df
        self.row_index = row_index
        
    @property
    def index(self):
        return self.row_index

    @property
    def row(self):
        return self.df.iloc[self.row_index, :]

    def __str__(self):
        s = self.row.to_string()
        return s

    def pprint_row(self):
        data_dict = self.row.to_dict()
        data_type = self.df.dtypes.to_dict()
        table = Table(
            safe_box=True,
            show_lines=True
        )
        table.add_column('col_name', style='cyan', no_wrap=True)
        table.add_column('value', style='magenta')
        table.add_column('dtype', style='green')
        for k, v in data_dict.items():
            table.add_row(k, str(v), str(data_type[k]))
        console.print(table)

    def __setitem__(self, name, value):
        if isinstance(name, str):
            self.df.loc[self.row_index, name] = value
            return
        raise TypeError('Only int or str type allowed.')

    def __getitem__(self, name):
        if isinstance(name, str):
            return self.df.loc[self.row_index, name]
        raise TypeError('Only int or str type allowed.')


class PandasObject:

    def __init__(
        self,
        df: DataFrame
    ):
        self.df = df
        self.to_csv = df.to_csv
        self.to_excel = df.to_excel
        self.head = df.head
        self.tail = df.tail
        self.describe = df.describe
        self.groupby = df.groupby
        self.iloc = df.iloc
        self.loc = df.loc
        self.apply = df.apply
        self.applymap = df.applymap
        self.max = df.max
        self.min = df.min
        self.mean = df.mean
        self.fillna = df.fillna
        self.reset_index = df.reset_index

    @property
    def columns(self):
        return self.df.columns

    @property
    def dtypes(self):
        return self.df.dtypes

    def __getattr__(self, name: str):
        try:
            handle = object.__getattribute__(self, name)
        except AttributeError:
            df = object.__getattribute__(self, 'df')
            if hasattr(df, name):
                return getattr(df, name)
        else:
            return handle

        raise AttributeError('Attribute %s not found.' % name)

    def __getitem__(self, index):
        return self.df[index]

    def iter_by_row(self, query=None):
        if query is not None:
            df = self.df.query(query)
        else:
            df = self.df
        for i in range(df.shape[0]):
            yield PandasObjectRow(self.df, i)

    def __str__(self):
        return self.df.to_string()

