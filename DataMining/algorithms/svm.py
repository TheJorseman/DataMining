from sklearn import model_selection
from sklearn.svm import SVC 
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

from pandas import DataFrame, crosstab, read_table
import numpy as np  
import matplotlib.pyplot as plt
import random
from io import StringIO, BytesIO
from base64 import b64encode

from DataMining.tools.table_html import TableHTML
from DataMining.tools.html_tools import HTML_tools


class SVM(object):
    def __init__(self, df, input_vars, output_var, train_size, kernel):
        super().__init__()
        self.df = df
        self.input_vars = input_vars
        self.output_var = output_var
        self.train_size = train_size
        self.ndigits = 4
        self.model = SVC(kernel=kernel)
        self.replaced = {}
        self.clean_data()

    def clean_data(self):
        columns = self.output_var + self.input_vars
        # Se convierte la variable de salida a la establecida -1,1
        values_output = self.df[self.output_var[0]].unique()
        if len(values_output)>2:
            raise Warning("El sistema solo puede clasificar dos clases, cambie los datos o cambie la variable de salida.")
        new_vals = tuple(zip(values_output,[-1,1]))
        dict_vals = {value[0]:value[1]  for value in new_vals}
        self.replaced.update(dict_vals)
        self.df = self.df.replace(dict_vals)
        ##########################################################
        for column in columns:
            if self.df[column].dtypes == "O":
                values = self.df[column].unique()
                new_vals = tuple(zip(values,range(len(values))))
                dict_vals = {value[0]:value[1]  for value in new_vals}
                self.replaced.update(dict_vals)
                self.df = self.df.replace(dict_vals)
        

    def prepare_data(self):
        Y = self.df[self.output_var]
        X = self.df[self.input_vars]
        self.X_train, self.X_validation, self.Y_train, self.Y_validation = model_selection.train_test_split(X, Y, train_size=self.train_size, shuffle=True)

    def fit_model(self, html=False):
        self.prepare_data()
        self.model.fit(self.X_train, self.Y_train.values.ravel())
        PrediccionesNuevas = self.model.predict(self.X_validation)
        confusion_matrix = crosstab(self.Y_validation.values.ravel(), PrediccionesNuevas, rownames=['Real'], colnames=['Predicción'])
        score = self.model.score(self.X_validation, self.Y_validation)
        report = classification_report(self.Y_validation, PrediccionesNuevas)
        print(report)
        if html:
            return self.response_html(confusion_matrix, score, report, self.model.intercept_, self.model.coef_)
        return self.response_dict(confusion_matrix, score, report, self.model.intercept_, self.model.coef_)
        
    def response_dict(self, confusion_matrix, score, report, intercept, coef):
        response = {}
        response["confusion_matrix"] = confusion_matrix
        response["score"] = score
        response["report"] = report
        response["intercept"] = intercept.tolist()
        response["coef"] = coef.tolist()
        return response

    def replaced_html(self):
        text = "<strong>{}:</strong> <span>{}</span><br>"
        result = "<strong>Las siguientes variables han cambiado de valor para procesar los datos:</strong><br>"
        for old,new in self.replaced.items():
            result += text.format(old,new)
        return result

    def response_html(self, confusion_matrix, score, report, intercept, coef):
        response = {}
        header = "<h6>{}</h6>"
        text = "<strong>{}:</strong> <span>{}</span>"
        text_inv = "<span>{}</span><strong>*{}</strong> "
        table_sm = """<div class="row"><div class="col-5">{}</div></div>"""
        report_df = self.parse_report(report)
        response["report"] =header.format("Reporte") + table_sm.format(report_df.to_html(classes="table table-bordered table-sm", index=False)).replace("dataframe","")
        confusion_df = self.parse_confussion_matrix(confusion_matrix)
        response["confusion"] = header.format("Matriz de Clasificación") + table_sm.format(confusion_df.to_html(classes="table table-bordered table-sm", index=False)).replace("dataframe","")
        response["score"] = text.format("Score",score)
        response["changed_vals"] = self.replaced_html()
        response["html-join"] = "<br>".join(v for v in response.values())
        response["intercept"] = intercept[0].tolist()
        response["coef"] = coef[0].tolist()
        return response


    def parse_confussion_matrix(self, confusion_matrix):
        matrix = confusion_matrix.to_numpy()
        columns = [" "] + ["Pred "+str(val) for val in confusion_matrix.columns.values]
        data = []
        for i in range(len(matrix)):
            data.append( ["VReal " + str(i)] + matrix[i].tolist())
        return DataFrame(data=data, columns=columns)

    def parse_report(self, report):
        report = report.split("\n")
        columns = [" "] + [ col for col in report[0].strip().split(" ") if col != ""]
        columns = self.translate_report(columns)
        data = []
        for row in report[1:]:
            if row != "":
                row_data = [r for r in row.strip().split("  ") if r != ""]
                if "accuracy" in row_data:
                    row_data = [row_data[0]] + ["-","-"] + row_data[1:]
                row_data = self.translate_report(row_data)
                data.append(row_data)
        return DataFrame(data, columns=columns)

    def translate_report(self,term_list):
        terms = {"precision": "Precisión", "recall": "Sensibilidad", "support": "Soporte", "accuracy": "Exactitud" }
        return [terms[key] if key in terms else key for key in term_list]
    
    def get_model_data(self):
        config = {}
        config["inputs"] = self.input_vars
        config["output"] = self.output_var
        config["replaced"] = self.replaced
        config["replaced_html"] = self.replaced_html()
        data = {}
        data["model"] = self.model
        data["config"] = config
        return data