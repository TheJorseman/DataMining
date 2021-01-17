from DataMining.tools.reader import Reader
from DataMining.tools.table_html import TableHTML
from sklearn.utils import shuffle
from DataMining.tools.html_tools import HTML_tools
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
        response["head"] = reader.get_head().to_html().replace("dataframe","table table-bordered")
        return response

    def get_columns(self):
        if self.header:
            return self.reader.get_columns()
        else:
            return ""

    def get_current_columns_html(self, table_id="table"):
        table = TableHTML(table_class="table ",table_id=table_id)
        columns = ["Columna"] + list(self.df.columns.values)
        table.set_head(columns)
        record = ["Incluir"] + self.get_record_html(list(self.df.columns.values))
        table.add_record(record)
        return table.get_html_table()

    def get_current_columns(self):
        return list(self.df.columns.values)

    def get_record_html(self,columns):
        template = """
        <div class="form-check">
            <input type="checkbox" id="{r_id}" class="form-check-input" name="{r_name}" value="{r_value}" checked>
        </div>
        """
        html = []
        for column in columns:
            html.append(template.format(r_id=column,r_name=column,r_value=column))
        return html

    def set_columns(self,columns):
        if self.table:
            self.df = self.df.drop(columns,axis=1)

    def set_rows(self,n_rows, n_shuffle=False):
        self.df = self.df.head(n_rows)
        if n_shuffle:
            self.df = shuffle(self.df)

    def get_selected_columns_html(self):
        current_columns = list(self.df.columns.values) 
        columns_table = TableHTML(table_class="table-sm table-bordered")
        columns_table.add_record(current_columns)
        return columns_table.get_html_table()

    def get_summary(self):
        summary = {}
        summary["sel_columns_html"] = self.get_selected_columns_html()
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


    def get_options_html(self):
        columns = list(self.df.columns.values) 
        html_code = ""
        for column in columns:
            html_code += HTML_tools.option_html(column,column)
        return html_code


        