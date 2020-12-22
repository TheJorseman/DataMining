# External Modules
from flask import Flask, render_template, request, jsonify, send_file, Response
import pandas as pd
from io import StringIO, BytesIO
from base64 import b64encode
import matplotlib
# Modules
from DataMining.tools.data_table_parser import CSV_reader
from DataMining.tools.apyori_parser import rules_to_html
from DataMining.tools.reader import Reader
from DataMining.tools.data_obj import Data
from DataMining.tools.table_html import TableHTML
from DataMining.algorithms.distance import Distance

# Configurations
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

def get_correlation_heatmap(matrix_correlation):
    from matplotlib import rcParams
    rcParams.update({'figure.autolayout': True})
    import seaborn as sb 
    pic_IObytes = BytesIO()
    heatmap = sb.heatmap(matrix_correlation, annot = True)
    # fix for mpl bug that cuts off top/bottom of seaborn viz
    b, t = plt.ylim() # discover the values for bottom and top
    b += 0.5 # Add 0.5 to the bottom
    t -= 0.5 # Subtract 0.5 from the top
    plt.ylim(b, t) # update the ylim(bottom, top) values
    ###########################################################
    figure = heatmap.get_figure()
    figure.savefig(pic_IObytes,format='png')
    pic_IObytes.seek(0)
    return b64encode(pic_IObytes.read())



@app.route("/pearson_correlation_heatmap", methods=["GET"])
def pearson_correlation_heatmap():
    response = {}
    if "DATA" in data_config:
        matrix_correlation = data_config["DATA"].df.corr(method='pearson')
        pic_hash = get_correlation_heatmap(matrix_correlation)
        response["heatmap_html"] = get_image_b64(pic_hash)
        plt.close()
    return jsonify(response)

@app.route("/get_current_columns", methods=["GET"])
def get_current_columns():
    response = {}
    if "DATA" in data_config:
        response["sel_columns_html"] = data_config["DATA"].get_current_columns_html()
        response["columns"] = data_config["DATA"].get_current_columns()
    return jsonify(response)

@app.route("/get_visualization_method", methods=["POST"])
def get_visualization_method():
    response = {}
    if "DATA" in data_config:
        response["visualization_method"] = None
        response["sel_columns_html"] = data_config["DATA"].get_current_columns_html()
        response["columns"] = data_config["DATA"].get_current_columns()
    return jsonify(response)

@app.route("/set_current_columns", methods=["POST"])
def set_current_columns():
    global data_config
    response = {}
    if "DATA" in data_config and request.form:
        form = dict(request.form) 
        data_config["DATA"].set_columns([k for k,v in form.items() if v == "false"])
        response["summary_columns"] = data_config["DATA"].get_selected_columns_html()
    return jsonify(response)

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
        response["html"] = TableHTML(table_class="table table-hover").apriori_table(rules)
    return jsonify(response)

@app.route("/correlation_process", methods=["POST"])
def correlation_process():
    response = {}
    if "DATA" in data_config:
        matrix_correlation = data_config["DATA"].df.corr(method='pearson')
        response["correlation_matrix_html"] = matrix_correlation.to_html().replace("dataframe","table")
        pic_hash = get_correlation_heatmap(matrix_correlation)
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

@app.route("/calc_distance", methods=["POST"])
def calc_distance():
    global data_config
    response = {}
    if request.form and "DATA" in data_config:
        method = request.form["metric"]
        distance = Distance(data_config["DATA"].df , dict(request.form))
        distance_table = distance.get_matrix_table()
        title = "<h5>Matriz de Distancias</h5>"
        response["distance_table"] = title + distance_table
        # Export Data #########################################
        data_config["EXPORT_FILE"] = distance.get_export_file()
        data_config["EXPORT_FILENAME"] = "distance_matrix.csv"
        #######################################################
    return jsonify(response)

@app.route("/export_table")
def export_table():
    csv = data_config["EXPORT_FILE"]
    export_name = "attachment; filename=" + data_config["EXPORT_FILENAME"]
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 export_name})


@app.route("/apriori")
def apriori():
    return render_template("apriori.html")

@app.route("/correlaciones")
def correlaciones():
    return render_template("correlation.html")

@app.route("/metricas")
def metricas():
    return render_template("metricas.html")

@app.route("/clustering")
def clustering():
    return render_template("clustering.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/")
def index():
    return render_template("index.html")

app.run(debug=True,port=8000)


#data = CSV_reader('apriori.csv',bool)
#print(data.df)

