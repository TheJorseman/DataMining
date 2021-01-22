from pandas import read_csv,read_excel,read_table
from DataMining.tools.table_html import TableHTML

class Reader(object):
    def __init__(self,path,filename, header, table):
        ext = filename.split(".")[-1]
        self.path = path
        self.filename = filename
        self.extensions = ["csv", "txt", "xlsx"]
        self.header = header
        self.table = table
        if ext.lower() == "csv":
            self.df = read_csv(path,header=0 if header else None)
        elif ext.lower() == "txt":
            self.df = read_table(path,header=0 if header else None)
        elif ext.lower() == "xlsx":
            self.df = read_excel(path,header=0 if header else None)
        else:
            raise Warning("Solo se admiten las extensiones " + ",".join(self.extensions))

    def get_head(self):
        return self.df.head()
    
    def set_columns(self,columns):
        pass

    def get_columns(self):
        return list(self.df.columns.values)

    def get_supported_ext(self):
        return self.extensions

    def get_df_len(self):
        return len(self.df.index)

    def select_columns_html(self):
        if self.table:
            table = TableHTML()
            columns = ["Columna"] + self.get_columns()
            table.set_head(columns)
            record = ["Incluir"] + self.get_record_html(self.get_columns())
            table.add_record(record)
            return table.get_html_table()
        else:
            return ""

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