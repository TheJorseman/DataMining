from pandas import read_csv
from collections import Counter
from numba import jit
#import numpy as np
class CSV_reader(object):

    matrix = None
    remove_data_type = object

    def __init__(self,filename,remove_first_column=False):
        self.filename = filename
        self.df = read_csv(filename)
        self.dtype = Counter(self.df.dtypes).most_common(1)[0][0].name
        if self.dtype == 'object':
            self.apyori = self.get_apyori_data_object()
        else:
            if remove_first_column:
                self.df = self.get_valid_data(remove_null=True)
            self.apyori = self.get_apyori_data_numeric_bool()


    def get_apyori_data_numeric_bool(self):
        columns = list(self.df.columns.values)
        transactions = []
        transactions.append(columns)
        n_rows,n_columns = self.df.shape
        self.n_rows = n_rows
        self.n_columns = n_columns
        all_trans = self.get_matrix_from_df(bool)
        for t in range(n_rows):
            transactions.append([str(columns[j]) if all_trans[t,j] else 'nan' for j in range(n_columns)])           
        return transactions

    def get_apyori_data_object(self):
        transactions = []
        transactions.append(list(self.df.columns.values))
        n_rows,n_columns = self.df.shape
        self.n_rows = n_rows
        self.n_columns = n_columns
        for t in range(n_rows):
            transactions.append([str(self.df.values[t,j]) for j in range(n_columns)])
        return transactions

    def get_valid_data(self, remove_null=True):
        types = self.df.dtypes.tolist()
        if  object in types:
            headers = list(self.df.columns.values)
            columns = [headers[i] for i, x in enumerate(types) if x == object]
            self.df = self.df.drop(columns,axis=1)
        if remove_null:
            return self.df.dropna(how='all')

    def get_matrix_from_df(self, dtype):
        return self.df.to_numpy(dtype=dtype)

    def get_matrix(self,only_numbers=True):
        if only_numbers:
            return self.matrix(self.matrix != self.matrix.astype(float))
        return self.matrix

