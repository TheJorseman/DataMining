from scipy.spatial import distance
from numpy import ones
from pandas import DataFrame
from io import StringIO

class Distance(object):
    methods_dict = {"euclidean": distance.euclidean,"chebyshev": distance.chebyshev, "manhattan": distance.cityblock, "minkowski": distance.minkowski}
    decimal_round = 3
    def __init__(self, df, distance_dict):
        self.df = df
        self.method = distance_dict["metric"]
        self.minkowski_coef = False if not "minkowski_coef" in distance_dict else float(distance_dict["minkowski_coef"])
        self.calculate_distance_matrix()
    
    def calculate_distance(self, record_1, record_2):
        if self.method == "minkowski":
            return self.methods_dict[self.method](record_1,record_2,self.minkowski_coef)
        else:
            return self.methods_dict[self.method](record_1,record_2)

    def get_export_file(self):
        file = StringIO()
        self.matrix_df.round(self.decimal_round).to_csv(file)
        return file.getvalue()

    def get_matrix_table(self):
        return self.matrix_df.round(self.decimal_round).to_html(table_id="distance_table").replace("dataframe","table table-bordered")

    def calculate_distance_matrix(self):
        shape = self.df.shape
        n_rows = shape[0]
        matrix = ones((n_rows, n_rows))
        for row in range(n_rows - 1):
            for column in range(row + 1, n_rows):
                matrix[row][column] = self.calculate_distance(self.df.iloc[row].to_numpy(),self.df.iloc[column].to_numpy())
        # Fill the other matrix side
        for row in range(1,n_rows):
            for column in range(row):
                matrix[row][column] = matrix[column][row]
        self.distance_matrix = matrix
        self.matrix_df = DataFrame(data=matrix, columns=range(n_rows))
