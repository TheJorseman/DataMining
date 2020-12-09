from DataMining.tools.reader import Reader
from DataMining.tools.table_html import TableHTML
from sklearn.utils import shuffle
from io import StringIO

class Data(object):
    def __init__(self, file, filename, header, table):
        self.file = file
        self.filename = filename
        self.header = header
        self.table = table
        self.reader = Reader(StringIO(file),filename,header,table)
        self.df = self.reader.df
        self.origin_df = self.reader.df.copy()

    def get_dict_data_analize(self):
        response = {}
        reader = self.reader
        response["sel_columns_html"] = reader.select_columns_html() if self.header else ""
        response["df_len"] = reader.get_df_len()
        response["head"] = reader.get_head().to_html().replace("dataframe","table")
        return response

    def get_columns(self):
        if self.header:
            return self.reader.get_columns()
        else:
            return ""

    def set_columns(self,columns):
        self.df = self.df.drop(columns,axis=1)

    def set_rows(self,n_rows,n_shuffle=False):
        self.df = self.df.head(n_rows)
        if n_shuffle:
            self.df = shuffle(self.df)

    def get_summary(self):
        summary = {}
        current_columns = list(self.df.columns.values) 
        columns_table = TableHTML(table_class="table-sm")
        columns_table.add_record(current_columns)
        summary["sel_columns_html"] = columns_table.get_html_table()
        summary["df_len"] = len(self.df.index)
        summary["filename"] = self.filename
        return summary

    def get_matrix_from_df(self, dtype):
        return self.df.to_numpy(dtype=dtype)

    def get_apyori_data_numeric_bool(self):
        columns = list(self.df.columns.values)
        transactions = []
        transactions.append(columns)
        n_rows,n_columns = self.df.shape
        all_trans = self.get_matrix_from_df(bool)
        for t in range(n_rows):
            transactions.append([str(columns[j]) if all_trans[t,j] else 'nan' for j in range(n_columns)])           
        return transactions

    def get_apyori_data_object(self):
        transactions = []
        transactions.append(list(self.df.columns.values))
        n_rows,n_columns = self.df.shape
        for t in range(n_rows):
            transactions.append([str(self.df.values[t,j]) for j in range(n_columns)])
        return transactions

    def get_apyori_list(self):
        if not self.table:
            self.apyori = self.get_apyori_data_object()
        else:
            self.apyori = self.get_apyori_data_numeric_bool()
        return self.apyori 
