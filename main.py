from DataMining.tools.data_table_parser import CSV_reader
from flask import Flask, render_template, request, jsonify
import pandas as pd
from io import StringIO, BytesIO
from base64 import b64encode
from DataMining.tools.data_table_parser import CSV_reader
from DataMining.tools.apyori_parser import rules_to_html
from DataMining.tools.reader import Reader
from DataMining.tools.data_obj import Data
from DataMining.tools.table_html import TableHTML
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask("Data Mining")
app.config["DATA_UPLOAD"] = "/uploads"
data_config = {}

def get_image_b64(b64encoded):
    image = """
        <img src="data:image/png;base64,{b64}"/>
    """
    return image.format(b64=b64encoded.decode("utf-8"))

@app.route("/apriori_process", methods=["POST"])
def apriori_process():
    response = {}
    if request.form and "DATA" in data_config:
        min_sup = float(request.form["support"])/100
        min_conf = float(request.form["confidence"])/100
        min_lif = float(request.form["lift"])
        from apyori import apriori
        rules = apriori(data_config["DATA"].get_apyori_list(), min_support=min_sup, min_confidence=min_conf, min_lift=min_lif, min_length=2)
        rules = list(rules)
        #min_rules = 10 if len(rules)> 10 else len(list(rules))
        response["html"] = TableHTML(table_class="table table-hover").apriori_table(rules)
    return jsonify(response)

@app.route("/correlation_process", methods=["POST"])
def correlation_process():
    response = {}
    if "DATA" in data_config:
        matrix_correlation = data_config["DATA"].df.corr(method='pearson')
        response["correlation_matrix_html"] = matrix_correlation.to_html().replace("dataframe","table")
        import seaborn as sb 
        pic_IObytes = BytesIO()
        figure = sb.heatmap(matrix_correlation, annot = True).get_figure()
        figure.savefig(pic_IObytes,format='png')
        pic_IObytes.seek(0)
        pic_hash = b64encode(pic_IObytes.read())
        response["heatmap_html"] = get_image_b64(pic_hash)
        plt.close()
        response["options"] = data_config["DATA"].get_options_html()
    return jsonify(response)

@app.route("/analize_data", methods=["POST"])
def analize_data():
    global data_config
    response = {}
    if request.files:
        file = request.files["file"].read().decode("utf-8")
        filename = request.files["file"].filename
        header = True if "header" in request.form else False
        table = True if "is_table" in request.form else False
        data_config = {"DATA" : Data(file,filename,header,table)}
        response = data_config["DATA"].get_dict_data_analize()
        response["columns"] = data_config["DATA"].get_columns()
    else:
        raise Warning("No se ha seleccionado un archivo")
    return jsonify(response)

@app.route("/save_conf", methods=["POST"])
def save_conf():
    global data_config
    form = dict(request.form) 
    nrows = int(form.get("len",0))
    form.pop("len")
    shuffle = False
    if "random" in form:
        shuffle = True
        form.pop("random")
    data_config["DATA"].set_rows(nrows,n_shuffle=shuffle)
    data_config["DATA"].set_columns([k for k,v in form.items() if v == "false"])
    return jsonify(data_config["DATA"].get_summary())

@app.route("/plot_graph", methods=["POST"])
def plot_graph():
    global data_config
    response = {}
    abcisa = request.form["abcisa"]
    ordenada = request.form["ordenada"]
    df = data_config["DATA"].df
    pic_IObytes = BytesIO()
    figure = plt.figure()
    plt.plot(df[abcisa],df[ordenada], 'bo')
    plt.ylabel(abcisa)
    plt.xlabel(ordenada)
    figure.savefig(pic_IObytes,format='png')
    pic_IObytes.seek(0)
    pic_hash = b64encode(pic_IObytes.read())
    response["plot"] = get_image_b64(pic_hash)
    plt.close()
    return jsonify(response)

@app.route("/apriori")
def apriori():
    #summary = data_config["DATA"].get_summary()
    return render_template("apriori.html")

@app.route("/correlaciones")
def correlaciones():
    return render_template("correlation.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/")
def index():
    return render_template("index.html")

app.run(debug=True,port=8000)


#data = CSV_reader('apriori.csv',bool)
#print(data.df)

