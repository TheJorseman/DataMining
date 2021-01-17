from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, max_error
import numpy as np  
import matplotlib.pyplot as plt
import random
from io import StringIO, BytesIO
from base64 import b64encode

from DataMining.tools.table_html import TableHTML
from DataMining.tools.html_tools import HTML_tools

class LinearReg(object):
    def __init__(self, df, input_vars, output_var):
        super().__init__()
        self.df = df
        self.input_vars = input_vars
        self.output_var = output_var
        self.ndigits = 4
        self.model = LinearRegression()

    def fit_model(self, html=False):
        X_train = np.array(self.df[self.input_vars])
        Y_train = np.array(self.df[self.output_var])
        self.model.fit(X_train, Y_train)
        Y_pronostico = self.model.predict(X_train)
        self.Y_pronostico = Y_pronostico
        model_data = {}
        model_data["coeficients"] = self.model.coef_
        model_data["intercept"] = self.model.intercept_
        model_data["residual_error"] = round(max_error(Y_train, Y_pronostico),self.ndigits)
        model_data["r2_score"] = round(r2_score(Y_train, Y_pronostico))
        if html:
            model_data["model_str"] = self.get_string_model_html(self.model.coef_[0], self.model.intercept_, model_data["residual_error"])
            return self.get_readable_model_data_html(model_data)
        model_data["model_str"] = self.get_string_model(self.model.coef_[0], self.model.intercept_, model_data["residual_error"])
        return self.get_readable_model_data(model_data)

    def get_string_model(self, coef, intercept, residual_error):
        coef_str = " ".join(["{}{}*{}".format("+" if coef[i]>0 else "", coef[i], self.input_vars[i])  for i in range(len(coef))])
        return "{} = {} {} {}".format(self.output_var[0], float(intercept[0]), coef_str, ("+" if residual_error > 0 else "")+ str(residual_error))

    def get_string_model_html(self, coef, intercept, residual_error):
        coef_str = " ".join(["{}{}*<strong>{}</strong>".format("+" if coef[i]>0 else "", coef[i], self.input_vars[i])  for i in range(len(coef))])
        return "<strong>{}</strong> = {} {} {}".format(self.output_var[0], float(intercept[0]), coef_str, ("+" if residual_error > 0 else "")+ str(residual_error))

    def get_readable_model_data(self,data):
        response = {}
        response["coeficients"] = 'Coeficientes: {} '.format(" ".join(str(coef) for coef in data["coeficients"][0]))
        response["intercept"] =  'Intercepto: {} '.format(str(float(data["intercept"][0])))
        response["residual_error"] = "Error residual: ".format(data["residual_error"])
        response["r2_score"] = "Bondad de ajuste (Score): {}".format(data["r2_score"])
        response["model_str"] = "Modelo: {}".format(data["model_str"])
        return response

    def get_readable_model_data_html(self,data):
        response = {}
        response["coeficients"] = '<strong>{}</strong><span> {}</span><br>'.format("Coeficientes: "," ".join(str(coef) for coef in data["coeficients"][0]))
        response["intercept"] =  '<strong>{}</strong><span> {}</span><br>'.format("Intercepto:", str(float(data["intercept"][0])))
        response["residual_error"] = "<strong>{}</strong><span> {}</span><br>".format("Error residual: ",data["residual_error"])
        response["r2_score"] = "<strong>{}</strong><span> {}</span><br>".format("Bondad de ajuste (Score):",data["r2_score"])
        response["model_str"] = "<strong>{}</strong><br><span> {}</span><br>".format("Modelo:",data["model_str"])
        response["html_join"] = " ".join(item for item in response.values() )
        return response

    def get_columns(self):
        return list(self.df.columns.values) + ["Y_pronostico"]

    def get_columns_html(self, table_id="table"):
        table = TableHTML(table_class="table ",table_id=table_id)
        columns = ["Columna"] + self.get_columns()
        table.set_head(columns)
        record = ["Incluir"] + self.get_record_html(self.get_columns())
        table.add_record(record)
        return table.get_html_table()

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

    def get_options_html(self):
        columns = self.get_columns()
        html_code = ""
        for column in columns:
            html_code += HTML_tools.option_html(column,column)
        return html_code

    def inference(self, value_list):
        x = np.array(value_list)
        return self.model.predict(x)

    def plot(self, y, x_s):
        self.df.sort_index(inplace=True)
        figure = plt.figure(figsize=(15, 5))
        colors = ['green',"blue", "red","cyan","magenta","yellow","black"]
        for i in range(len(x_s)):
            if i > len(colors):
                color = random.choice(colors)
            else:
                color = colors[i]
            if x_s[i] == "Y_pronostico":
                plt.plot(self.df[y], self.Y_pronostico, color=color, marker='o', label='Pronóstico')
                continue
            plt.plot(self.df[y], self.df[x_s[i]], color=color, marker='o', label=x_s[i])
        plt.grid(True)
        plt.legend()
        pic_IObytes = BytesIO()
        figure.savefig(pic_IObytes,format='png')
        pic_IObytes.seek(0)
        return b64encode(pic_IObytes.read())


    def get_model_data(self):
        config = {}
        config["inputs"] = self.input_vars
        config["output"] = self.output_var
        data = {}
        data["model"] = self.model
        data["config"] = config
        return data
