from numpy import zeros, array, delete
from itertools import combinations
from numba import jit
import time 
from DataMining.tools.data_table_parser import CSV_reader

class Rule(object):
    def __init__(self):
        pass


class Apriori(object):
    def __init__(self, df, min_supp=0, min_conf=0, min_lift=0, min_k=2):
        self.df = df
        self.items = list(df.columns.values)
        self.min_supp = min_supp
        self.min_conf = min_conf
        self.min_lift = min_lift
        self.min_k = min_k
        self.column_dict = {k:v for v,k in enumerate(self.items)}
        self.rules = []
        self.frequency = []
    
    def columns_to_numbers(self,value):
        return self.column_dict[value]

    def get_items(self, current_items, k):
        items = list(combinations(current_items,k+1))
        item_list = [list(map(self.columns_to_numbers,list(item))) for item in items]
        return items, array(item_list)

    def apriori(self):
        current_items = self.df.columns.values
        matrix = self.get_matrix_from_df(bool)
        for k in range(3):
            items,items_vector = self.get_items(current_items,k)
            supp_vector = get_items_supp(items_vector, matrix)
            names,vector = self.get_support_min_vector(items, supp_vector)
            print(names, vector)
            current_items = self.get_unique_items(names,items)
            if k == 0:
                self.frequency = supp_vector
            else:
                self.create_rules(names,vector)
            #print(names, vector)

    def create_rules(self,names,vector):
        n_rules = len(names)
        n = self.df.shape[0]
        for r in range(n_rules):
            support = vector[r]/n
            support_x =self.frequency[self.column_dict[names[r][0]]]
            confidence = vector[r]/support_x
            lift = support/1


    def get_unique_items(self, names, comb):
        items = []
        names = set([l for i in names for l in i])
        for item in comb:
            for col in item:
                if col not in items and col in names:
                    items.append(col)
        return items

          
    def get_support_min_vector(self, names, vector):
        v_len = vector.shape[0]
        new_vector = []
        new_names = []
        for i in range(v_len):
            if vector[i] >= self.min_supp:
                new_vector.append(vector[i])
                new_names.append(names[i])
        return new_names,array(new_vector)

    def get_matrix_from_df(self, dtype):
        return self.df.to_numpy(dtype=dtype)



@jit(nopython=True, parallel=True)
def get_items_supp(items,matrix):
    supp_vector = zeros(len(items))
    item_len = len(items[0])
    items_len =len(items)
    for n_column in range(items_len):
        for n_row in range(matrix.shape[0]):
            value = True
            column = items[n_column]
            for index in range(item_len):
                n_col = column[index]
                value = value and matrix[n_row][n_col]
            if value:
                supp_vector[n_column] += 1                    
    return supp_vector

